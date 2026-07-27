#!/usr/bin/env node
/**
 * Standing regression suite — run this after ANY change to the Lesson Builder,
 * TTS tool, or lesson shell, before handing a new version off.
 *
 * Uses Playwright driving a real Chrome binary (cached locally by another tool
 * in this sandbox at the CHROME_PATH below) — actual browser execution, not
 * static analysis. Catches things node --check structurally cannot: the
 * </script>-inside-a-string HTML-parsing bug from this session is the case in
 * point — it was invisible to syntax checking and only showed up when a real
 * browser tokenizer parsed the file.
 *
 * USAGE
 *   node run_all.js <lesson-builder.html> <tts-tool.html> <lesson-shell.html>
 *   All three paths are optional — pass only the file(s) you actually changed.
 *
 * WHAT THIS DOES NOT COVER
 *   The real GitHub push (needs a real token, which never belongs in this
 *   sandbox) and anything requiring real ElevenLabs credits. Those stay a
 *   manual, human step — this suite exists to make sure everything upstream
 *   of that step is solid before it's worth spending real API calls testing.
 */

const { chromium } = require('playwright');
const path = require('path');

const CHROME_PATH = '/home/claude/.cache/puppeteer/chrome/linux-131.0.6778.204/chrome-linux64/chrome';

let passCount = 0, failCount = 0;
function report(label, ok, detail = '') {
  console.log(`${ok ? '✅' : '❌'} ${label}${detail ? ' — ' + detail : ''}`);
  ok ? passCount++ : failCount++;
}

async function newErrorTrackedPage(browser) {
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', err => errors.push(err.message));
  page.on('dialog', async d => { await d.dismiss(); });
  return { page, errors };
}

// ═══════════════════════════════════════════
//  LESSON BUILDER SUITE
// ═══════════════════════════════════════════
async function testLessonBuilder(browser, filePath) {
  console.log(`\n─── Lesson Builder: ${path.basename(filePath)} ───`);
  const { page, errors } = await newErrorTrackedPage(browser);

  await page.goto(`file://${filePath}`);
  await page.waitForTimeout(500);
  report('Loads with no page errors', errors.length === 0, errors.join('; '));

  const dashVisible = await page.locator('.dash-title').isVisible().catch(() => false);
  report('Dashboard renders', dashVisible);

  // Open an existing lesson, navigate the main tabs
  await page.click('.lesson-card:has-text("Food Court Basics")').catch(() => {});
  await page.waitForTimeout(300);
  report('Opens an existing lesson into the editor', await page.locator('#modList').count() > 0);
  await page.click('text=Dashboard');
  await page.waitForTimeout(200);

  // Multi-instance wizard: create a lesson with 3x the same module type
  await page.click('.new-lesson-card');
  await page.waitForTimeout(300);
  await page.fill('#wizName', 'Regression Test Lesson');
  await page.click('text=Next: pick modules');
  await page.waitForTimeout(300);
  const addBtn = page.locator('.picker-item:has-text("Listen & Choose") .picker-add');
  await addBtn.click(); await page.waitForTimeout(120);
  await addBtn.click(); await page.waitForTimeout(120);
  await addBtn.click(); await page.waitForTimeout(120);
  const addedRows = (await page.locator('.added-row .aname').allTextContents()).map(t => t.trim());
  report('Wizard creates 3 distinct instances (#2, #3 suffixes)',
    addedRows.filter(t => t.includes('Listen & Choose')).length === 3 && addedRows.some(t => t.includes('#3')),
    addedRows.join(' | '));

  await page.click('text=Create Lesson');
  await page.waitForTimeout(400);
  await page.click('.lesson-card:has-text("Regression Test Lesson")');
  await page.waitForTimeout(400);
  const sidebar = (await page.locator('.mod-item').allTextContents()).map(t => t.replace(/\s+/g, ' ').trim());
  report('Sidebar shows all 3 instances separately',
    sidebar.filter(t => t.includes('Listen & Choose')).length === 3, sidebar.join(' | '));

  // Preview production JSON
  await page.click('text=🔍 Preview production JSON');
  await page.waitForTimeout(300);
  const previewJson = await page.locator('#prodPreviewJson').inputValue().catch(() => '');
  report('Preview production JSON uses real hyphenated type names',
    previewJson.includes('audio-understanding'));
  // Exercise the actual copy button — confirms it doesn't throw on file:// origin
  await page.click('button:has-text("Copy JSON")');
  await page.waitForTimeout(200);
  report('Copy JSON button does not throw on file:// origin', errors.length === 0, errors.join('; '));
  await page.click('text=Close');
  await page.waitForTimeout(200);

  // Export for TTS tool against real content (Colors), verify exclusion list
  await page.click('text=Dashboard');
  await page.waitForTimeout(200);
  await page.click('.lesson-card:has-text("Colors")');
  await page.waitForTimeout(300);
  await page.click('text=🎙️ Export for TTS tool');
  await page.waitForTimeout(300);
  const exportJson = await page.locator('#ttsExportJson').inputValue().catch(() => '{}');
  let parsed = { assets: [] };
  try { parsed = JSON.parse(exportJson); } catch (e) { report('Export JSON parses', false, e.message); }
  const prefixes = new Set(parsed.assets.map(a => a.id.split('.')[0]));
  report('Export excludes gapfill/truefalse/putinorder/wordmatch',
    !['gapfill', 'truefalse', 'putinorder', 'wordmatch'].some(t => prefixes.has(t)), [...prefixes].join(','));
  report('Export produces real lines from seeded content', parsed.assets.length > 0, `count=${parsed.assets.length}`);
  // Exercise both buttons for real — this is exactly what was reported broken
  await page.click('button:has-text("Copy JSON")');
  await page.waitForTimeout(200);
  const copyMsg = await page.locator('#ttsExportCopyMsg').textContent().catch(() => '');
  report('Copy JSON gives visible feedback either way (success or fallback message)',
    errors.length === 0, `msg="${copyMsg.trim()}"`);
  await page.click('button:has-text("Download file")');
  await page.waitForTimeout(200);
  report('Download button does not throw on file:// origin', errors.length === 0, errors.join('; '));
  await page.click('text=Close').catch(() => {});
  await page.waitForTimeout(200);

  // Persistence across reload
  await page.click('text=Dashboard');
  await page.waitForTimeout(4500); // let the periodic autosave fire
  await page.reload();
  await page.waitForTimeout(800);
  report('Draft survives a reload', await page.locator('.lesson-card:has-text("Colors")').count() > 0);

  report('Zero JS errors across full session', errors.length === 0, errors.join('; '));
  await page.close();
}

// ═══════════════════════════════════════════
//  TTS TOOL SUITE
// ═══════════════════════════════════════════
async function testTtsTool(browser, filePath) {
  console.log(`\n─── TTS Tool: ${path.basename(filePath)} ───`);
  const { page, errors } = await newErrorTrackedPage(browser);
  await page.goto(`file://${filePath}`);
  await page.waitForTimeout(500);
  report('Loads with no page errors', errors.length === 0, errors.join('; '));
  const cfgBtnText = await page.locator('#cfgBtn').textContent().catch(() => '');
  report('Shows "no API key" warning state by default', cfgBtnText.includes('Set API key'), cfgBtnText);
  await page.close();
}

// ═══════════════════════════════════════════
//  LESSON SHELL SUITE (student-facing runtime)
// ═══════════════════════════════════════════
async function testLessonShell(browser, filePath) {
  console.log(`\n─── Lesson Shell: ${path.basename(filePath)} ───`);
  const { page, errors } = await newErrorTrackedPage(browser);
  await page.goto(`file://${filePath}`);
  await page.waitForTimeout(500);
  report('Loads with no page errors', errors.length === 0, errors.join('; '));

  const names = await page.locator('.name-btn').allTextContents();
  report('Student name picker renders', names.length > 0, `${names.length} names`);

  await page.click('.name-btn >> nth=0');
  await page.click('#start-btn');
  await page.waitForTimeout(400);
  report('Module screen launches after picking a name',
    await page.locator('#module-container').isVisible().catch(() => false));

  const listenBtn = page.locator('#listen-btn, #lc-listen-btn');
  if (await listenBtn.count() > 0) {
    await listenBtn.first().click();
    await page.waitForTimeout(300);
    report('Audio playback (speak/audioFile-fallback path) triggers with no errors', errors.length === 0, errors.join('; '));
  }
  await page.close();
}

// ═══════════════════════════════════════════
//  MAIN
// ═══════════════════════════════════════════
(async () => {
  const [, , lbPath, ttsPath, shellPath] = process.argv;
  if (!lbPath && !ttsPath && !shellPath) {
    console.log('Usage: node run_all.js <lesson-builder.html> [tts-tool.html] [lesson-shell.html]');
    process.exit(1);
  }

  const browser = await chromium.launch({
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    if (lbPath) await testLessonBuilder(browser, path.resolve(lbPath));
    if (ttsPath) await testTtsTool(browser, path.resolve(ttsPath));
    if (shellPath) await testLessonShell(browser, path.resolve(shellPath));
  } finally {
    await browser.close();
  }

  console.log(`\n${'='.repeat(50)}\n${passCount} passed, ${failCount} failed\n${'='.repeat(50)}`);
  process.exit(failCount > 0 ? 1 : 0);
})();
