{"objectType": smtSolver,
 "arguments":
 {
     'abstractConstr': [


         # ECG Boxes
         # First 35 Timestamps corresponding to the upper part in between 20
         # and 40:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[-2, 2], [-4, 1], [-4, 0], [-5, -1], [-5, -1], [-4, -1], [-3, -1], [-3, -1], [-2.5, -0.5], [-2, 0], [-1.5, 0], [-1.5, 0.5], [-1, 0.5], [-1, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [0, 0.5], [0, 0.5], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
         },
         # First 35 Timestamps corresponding to the lower part in between 20
         # and 40:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[-2, 2], [-4, 1], [-4, 0], [-5, -1], [-5, -1], [-4, -1], [-3, -1], [-3, -1], [-2.5, -0.5], [-2, 0], [-1.5, 0], [-1.5, 0.5], [-1, 0.5], [-1, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0], [-0.5, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0]]
         },
         # Timestamps 36-70 for the lower class:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[-1.5, -0.5], [-1.5, -0.5], [-1.5, -0.5], [-1.5, -0.5], [-1.5, -0.5], [-1.5, -0.5], [-1.5, -0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5]]
         },
         # Timestamps 36-70 for the upper class:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5]]
         },
         # Timestamps 71-105 for the bottom line:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
         },
         # Timestamps 71-105 for the upper peak:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0.5, 1.5], [0.5, 1.5], [0.5, 1.5], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]]
         },
         # Timestamps 106-140 for the bottom peak at and:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0.5, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1.5, 0.5], [-2, 0], [-2.5, -0.5], [-3, -1], [-3.5, -1.5], [-3.5, -1.5], [-3.5, -1.5], [-4, -2], [-4.5, -3.5], [-4, -2], [-4, -2], [-4, 2]]
         },
         # Timestamps 106-140 for the upper peak at end:
         {
             'adversAttack': {'severity': 2},
             'customBoundingBox': [[1, 2], [1, 2], [1, 2], [0.5, 1.5], [0.5, 1.5], [0.5, 1.5], [0, 1], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-0.5, 0], [-1, 1], [-1, 1], [-1, 1], [-0.5, 1], [0, 1], [0.5, 1.5], [1, 2], [1, 2], [1, 2], [1, 2], [0, 2], [0, 2], [0, 2], [-4, -2], [-4, 2]]
         },

     ],

     # # Sine Curve Boxes
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/algorithmInputLayerSize) - 0.1,math.sin((2*math.pi*x)/algorithmInputLayerSize)+0.1] for x in range(algorithmInputLayerSize)]
     # },
     # # {
     # # 'adversAttack': {'severity': 2},
     # # 'customBoundingBox' : [[math.sin((2*math.pi*x)/algorithmInputLayerSize) - 0.2,math.sin((2*math.pi*x)/algorithmInputLayerSize)+0.2] for x in range(algorithmInputLayerSize)]
     # # },

     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize)]
     # },
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize, 2*algorithmInputLayerSize)]
     # },
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(2*algorithmInputLayerSize, 3*algorithmInputLayerSize)]
     # },

     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.2,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.2] for x in range(algorithmInputLayerSize)]
     # },
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.2,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.2] for x in range(algorithmInputLayerSize, 2*algorithmInputLayerSize)]
     # },
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.2,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.2] for x in range(2*algorithmInputLayerSize, 3*algorithmInputLayerSize)]
     # },



     # ],

     # Growing Boxes with 0 at one end
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[0-(i+1)/50,0+(i+1)/50] for x in range(algorithmInputLayerSize)]
     # }
     # for i in range(5)
     # ],

     # Growing Boxes
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[0-(i+1)/10,0+(i+1)/10] for x in range(algorithmInputLayerSize)]
     # }
     # for i in range(13)
     # ],

     # Growing Boxes around a sineTrainPoint
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x)/numberSineCycles)-(i+1)/10,math.sin((2*math.pi*x)/numberSineCycles)+(i+1)/10] for x in range(algorithmInputLayerSize)]
     # }
     # for i in range(10)
     # ],


     # Moving Box through sine curve
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*x+i*5)/numberSineCycles)-0.2,math.sin((2*math.pi*x+i*5)/numberSineCycles)+0.2] for x in range(algorithmInputLayerSize)]
     # }
     # for i in range(10)
     # ],

     # Moving Box through Middle of sine curve
     # {
     # 'adversAttack': {'severity': 2},
     # 'customBoundingBox' : [[math.sin((2*math.pi*(x+0))/numberSineCycles)-0.2 + (i-3)/10*((math.sin((2*math.pi*(x+25))/numberSineCycles)-0.2) - (math.sin((2*math.pi*(x+0))/numberSineCycles)-0.2)),math.sin((2*math.pi*x+0)/numberSineCycles)+0.2+(i-3)/10*((math.sin((2*math.pi*(x+25))/numberSineCycles)-0.2) - (math.sin((2*math.pi*(x+0))/numberSineCycles)-0.2))] for x in range(algorithmInputLayerSize)]
     # }
     # for i in range(16)
     'numSolutions': [5],
     'boundaryAroundSolution': [0.1],
 }
 }
