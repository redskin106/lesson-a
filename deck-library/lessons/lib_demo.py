import sys; sys.path.insert(0,'/home/claude/work/lesson')
import sxl
spec=[
 {'m':'sort','phase':'STUDY','title':'Fill the gaps','bank':['have to','should','shouldn’t','don’t have to','mustn’t'],
  'rows':[{'pic':'sc2_1.jpg','end':('c3','eat spicy food.')},{'pic':'sc2_2.jpg','end':('c3','see a doctor.')},{'pic':'sc2_3.jpg','end':('c3','stay in bed.')},{'pic':'sc2_4.jpg','end':('c3','drive.')}]},
 {'m':'chat','phase':'STUDY','lines':[('N','Hello. What’s the problem?'),('P','I have a headache.'),('N',[('c4','Where',True),('c2','does',False),('c1','it',False),('c3','hurt?',True)]),('P','My head hurts.')],'bank':[('c4','Where'),('c3','hurt?'),('c4','When'),('c3','hurts')]},
 {'m':'contrast','phase':'STUDY','title':'Not the same!','left':{'label':'Not allowed','grad':'red','pic':'mu_1.jpg','chips':[('c1','You'),('c2','mustn’t'),('c3','drink alcohol.')]},'right':{'label':'Not needed','grad':'teal','pic':'mu_2.jpg','chips':[('c1','You'),('c2','don’t have to'),('c3','take it with food.')]}},
 {'m':'storyboard','phase':'STUDY','title':'Quack says','grad':'amber','panels':['hw_1.jpg','hw_2.jpg','hw_3.jpg'],'hidden_last':True,'prompt':('What','happens next?')},
]
sxl.build(spec,'/home/claude/work/lesson/lib_demo',pdf=None)
