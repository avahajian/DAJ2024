dimport numpy as np
import random
import time
import csv
import matplotlib.pyplot as plt


import FixedLotCode as FL


start = time.time()
np.random.seed(21)
cycle = 0
bestSolCycle = np.zeros(2)
replications = 0
best_solution_collection = []
best_solution_collection2 = []
best_solution = []

if __name__ == '__main__':
    while replications < 2:
        iteration = 0
        counter = 0
        cycle_iteration = 0
        i = 0
        cycle = 0
        n = 300
        k = 0.1
        
        f = open("Optimization_FixedLot_BAT02_1.csv", "a", newline="")
        writer = csv.writer(f)
        writer.writerow(("Reorder_Point", "Fixed_Lot","Total_Cost","Service_Level"))
    
        GraphValues = [[0 for m in range(3)] for j in range(n)]
    
        ###########################
        upperBound = [15000, 168]  #
        lowerBound = [2000, 30]  #
        ############################
    
        serviceLevel = 0
        
        "Change the below level to 0.95"
        while serviceLevel < 0.95:
            
            if replications >= 1:
                x_start = np.zeros(2)
                x_start[0] = best_solution[0]
                x_start[1] = best_solution[1]
                print(x_start)
                
            else:
                x_start = np.zeros(2)
                x_start[0] = np.random.randint(lowerBound[0], upperBound[0])
                x_start[1] = np.random.uniform(lowerBound[1], upperBound[1]) 
                
                print(x_start)
                
                # Initialize x
                x = np.zeros((n + 1, 2))
                x[0] = x_start
            initial_solution = np.zeros(2)
            initial_solution = x_start
    
            current_solution = initial_solution
            best_solution = initial_solution
            
            func = FL.Poolfunction(current_solution[0], current_solution[1])
            
            
            func = np.array(func)
            best_fitness = (func)[0]  # objFnBest[0]
            serviceLevel = (func)[1]  # objFnBest[1]
            print(best_fitness, serviceLevel)
            
            writer.writerow((x_start[0], np.floor(x_start[1]*60.0), best_fitness, serviceLevel))
    
        fs = np.zeros(n + 1)
        fs[0] = best_fitness
        fsL = np.zeros(n + 1)
        fsL[0] = serviceLevel
        best_Service_Level = serviceLevel
        record_best_fitness = []
        iteration = 0
        i = 0
        
        while n > 0.0:
            np.random.seed(n)
            iteration += 1
            print("Iteration, Replication", iteration, replications)
            current_solution = np.zeros(2)
    
            rand_x_1 = np.random.rand()
            rand_x_2 = np.random.rand()
            rand_y_1 = np.random.rand()
            rand_y_2 = np.random.rand()
    
            if rand_x_1 >= 0.5:
                x1 = k * rand_x_2
            else:
                x1 = -k * rand_x_2
    
            if rand_y_1 >= 0.5:
                y1 = k * rand_y_2
            else:
                y1 = -k * rand_y_2
    
            
            if cycle < 15 and (iteration - cycle_iteration >=100):
                current_solution[0] = np.random.randint(lowerBound[0], upperBound[0])
                current_solution[1] = (np.random.uniform(lowerBound[1], upperBound[1]))
            
            
            elif cycle >= 15:
                comparison = bestSolCycle == best_solution
                equal_arrays = comparison.all()
                # print(bestSolCycle, best_solution, comparison)
                if equal_arrays:
                    print("Cycle is 15 here")
                    if counter < 20:
                        current_solution[0] = np.random.randint(best_solution[0]*0.8, best_solution[0]*1.2)
                        current_solution[1] = (np.random.uniform(best_solution[1]*0.8, best_solution[1]*1.2))
                        counter += 1
                        print("Counter < 2", counter)
                    
                    elif counter >=20 and counter < 60:
                        current_solution[0] = np.random.randint(best_solution[0]*0.6, best_solution[0]*1.4)
                        current_solution[1] = (np.random.uniform(best_solution[1]*0.6, best_solution[1]*1.4)) 
                        counter += 1
                        print("Counter >=2", counter)
                    
                    else:
                        current_solution[0] = (np.random.randint(lowerBound[0], upperBound[0]))
                        current_solution[1] = (np.random.uniform(lowerBound[1], upperBound[1])) 
                
                
                else:
                    
                    current_solution[0] = abs((best_solution[0] + x1 * np.random.randint(lowerBound[0], upperBound[0])))
                    current_solution[1] = abs((best_solution[1] + y1 * np.random.uniform(lowerBound[1], upperBound[1])))
                    
            else:
                
                current_solution[0] = abs((best_solution[0] + x1 * np.random.randint(lowerBound[0], upperBound[0])))
                current_solution[1] = (abs(best_solution[1] + y1 * np.random.uniform(lowerBound[1], upperBound[1])))
                
    
            """"Select the Production system that needs to be run"""
            
            func = FL.Poolfunction(current_solution[0], current_solution[1])
        
            func = np.array(func)
            current_fitness = (func)[0]  # objFnCurr[0]
            serviceLevel = (func)[1]  # objFnCurr[1]

            
            "Change the below level to 0.95"
            
            if serviceLevel >= 0.95:
                if current_fitness >= best_fitness:
                    cycle += 1
                    print(cycle)
                    #print("Current fitness >= best fitness")
                    #print(current_fitness, best_fitness)
                    accept = False
                else:
                    cycle = 0
                    cycle_iteration = iteration
                    #print("Current fitness < best fitness")
                    #print(current_fitness, best_fitness)
                    accept = True  # accept better solution
                if accept:
                    best_solution = current_solution  # update the best solution
                    bestSolCycle = best_solution
                    best_fitness = current_fitness
                    best_Service_Level = serviceLevel
                    
            print("current_solution, best_solution")
            print(current_solution, best_solution, best_fitness)
            
            writer.writerow((current_solution[0], np.floor(current_solution[1]*60.0), current_fitness, serviceLevel))
            

            x[i + 1][0] = best_solution[0]
            x[i + 1][1] = best_solution[1]
            fs[i + 1] = best_fitness
            GraphValues[i][0] = abs(best_solution[0])
            GraphValues[i][1] = abs(best_solution[1])
            GraphValues[i][2] = abs(best_fitness)
            fsL[i + 1] = best_Service_Level
            i += 1
            n = n - 1  #* frac
            # print current_temperature
            record_best_fitness.append(best_fitness)

        # print solution
        print('Best solution: ' + str(abs(best_solution)))
        print('Best objective: ' + str(abs(best_fitness)))
        
#        f.close()
    
        plt.plot(x[:, 0], x[:, 1], 'y-o')
        plt.savefig('contour.png')
    
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.plot(fs, 'r.-')
        ax1.legend(['Total Cost Value'])
        ax2 = fig.add_subplot(212)
        ax2.plot(x[:, 0], 'b.-')
        ax2.plot(x[:, 1], 'g--')
        ax2.legend(['Reorder Point', 'Lead Time'])
    
        # Save the figure as a PNG
        plt.savefig('iterations.png')
    
        end = time.time()
        #print(f'Time: {time.time() - start}')

        
        replications += 1
        print("Replication completed", replications)
        best_solution_collection = np.append(best_solution_collection, best_solution)
        best_solution_collection2 = np.append(best_solution_collection2, best_fitness)
        print(best_solution_collection)
        print(best_solution_collection2)
        
    
