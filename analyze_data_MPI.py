from gutfit.experimentalneutrinomassmatrix import ExperimentalNeutrinoMassMatrix
from gutfit.type1and2seesaw_v4_SUSY import Type1And2SeeSaw_v4, Predictions
import examples.multinest_v4
from gutfit import parameterlist
from pymultinest import watch, analyse, plot


#a = Type1And2SeeSaw_v4()



#build OBS as a daughter class of Type... and then use the trick with sample

import optparse
import numpy as np

op = optparse.OptionParser(usage=__doc__)
opts, args = op.parse_args() ###look at it!!!!


def sample(x,E,S,PL,N,pnames):
    D = []
    T = []
    for _ in range(N):
        p=PL()
#        from IPython import embed
#        embed()
#        exit(0)
        for num, pn in enumerate(pnames):
            p[pn] = x[num]
        data = E(p)
#        foundgoodpoint=False
#        while not foundgoodpoint:
#            if trials>1000000:
#                return D,T,False
#            p=PL()
##            print(pnames, len(pnames))
##            from IPython import embed
##            embed()
##            exit(1)
#            for num, pn in enumerate(pnames):
#                p[pn] = x[num]
#            if S.constraint(p):
#                foundgoodpoint = True
#            trials+=1
        theo = S(p)
       # print(theo)
        D.append(data)
        T.append(theo)
    return D, T, True



def load_parameter2():
    N_throwaway = 0 #make the code faster to test, set to zero for official esults
    points = np.loadtxt("%s/GUTFIT.txt"%args[0])
#    oldscan = np.loadtxt("ParaTable_10.txt")
   # N = len(points[0,:]);
    likelihood = points[N_throwaway:,1]
    Parameters = points[N_throwaway:,2:]
    #print(x[-1])

#    print(len(likelihood))
    return Parameters, likelihood

def loadParaTable():
    print("Called it")
    Parameters = np.loadtxt("ParaTable.txt")
    # "a1 a2 r1 r2 ce cnu m0"
    for i in range(len(Parameters[:,0])):
        #Parameters[i,0] = 0.38218340
        Parameters[i,3] = Parameters[i,3]*(10**(-9))
 #       cnu = Parameters[i,6] 
  #      Parameters[i,6] = Parameters[i,7]
   #     Parameters[i,7] = cnu
    return Parameters

if __name__ == "__main__":
    PL = parameterlist.ParameterList.fromConfigFile(args[1])#"examples/param_card.dat")
    Parameters, likelihood= load_parameter2()
    # x = Visualize.evaluate(parameters)
    #Parameters = loadParaTable()
    #print(Parameters[0,:])
    rank=0
    O = Predictions()
    E = ExperimentalNeutrinoMassMatrix()
        
    usethese = []
    Observations = []
    bounds, pnames = PL.getBox(usethese)
    for i in range(0,len(likelihood)):
        if (likelihood[i]/2) < 10:
            PP = [Parameters[i,j] for j in range(len(pnames))]
            print("Nr. of points: %f"%i)

            # print(PP)
            # print("Parameters up here")
            D, T, isgood = sample(PP,E, O, PL, 1, pnames)
            Observations.append(T[0])
            if i == 109482: 
                print(T.MnuTheory())
            #print(T[0])
            #print(Observations[0])
            #print(T[0])[13:15]
    if rank == 0:
        Observations = np.asarray(Observations)
        np.savetxt('%s/GUTFITpredictions.txt'%args[0], Observations)
        np.savetxt('%s/GUTFITpara.txt'%args[0],Parameters)
        np.savetxt('%s/GUTFITlikelihood.txt'%args[0],likelihood)                                                                                                                                           
    #   print("Predictions saved in: %s/GUTFITpredictions.txt") 
 #   	np.savetxt('%s/GUTFITpredictions.txt'%args[0], Observations)
  #  	np.savetxt('%s/GUTFITpara.txt'%args[0],Parameters)
   # 	np.savetxt('%s/GUTFITlikelihood.txt'%args[0],likelihood)
    #	print("Predictions saved in: %s/GUTFITpredictions.txt")
    
    #	print("Parameters saved in: %s/GUTFITpara.txt")
    
    #	print("Likelihood saved in: %s/GUTFITlikelihood.txt")
    	#plot
    
    
