
import simpy as sim
import numpy as np
import decimal, math
import time
import csv
import matplotlib.pyplot as plt

tCC = 0
avgServiceLevel = 0
start = time.time()
# global_uptime_array = []
starting_inventory = []



def RunQRcode(reOrderPoint, leadtime):
    global tCC, avgServiceLevel, global_uptime_array, demandarray, running_inventoryLevel
    global demands12, demandRate
    
    np.random.seed(111)
    nrep = 0
    rep = 10
    inhere = 0
    
    tCC = 0
    Pcost = 0
    Ocost = 0
    Icost = 0
    avgServiceLevel = 0
    totalUnitsProduced = 0
    Tidletime = 0
    tCC_array = []
    avgServiceLevel_array = []
    
    avgInventory = []
    avgOrder = []
    avgLostSales = []
    
    # f = open("QROutput_FixedTime.csv", "a", newline="")
    # writer = csv.writer(f)
    # writer.writerow(("TNow","Demand","Inventory After Demand", "Production Start Time", "Production", "Production End Time", "Production Length","Inventory after Production", "Daily Production", "WAiting Time"))
    
    
    
    while nrep < rep:  
        demands12 = 0
        demandRate = 900.0
        global_uptime_array = []
        JPH = 60.0
        leadTime = abs(leadtime)
        reorderPoint = abs(reOrderPoint)
    
        fixedCost = 227
        inventoryCost = 1.5
        penaltyCost = 50
        
        demandarray = []
        running_inventoryLevel = []
    
        
        signal = 0
        global totalDemandArrival, inventoryLevel, shortage, orders, totalIdleTime,variableRepairTime
        global nextDemandArrivalTime, demnCV, arrivalHours
        totalIdleTime = 0
        totalDemandArrival = 0
        inventoryLevel = reorderPoint
        shortage = 0
        orders = 0
        variableRepairTime = 0
        nextDemandArrivalTime = 0
        
        tup  = tuple()
        
        #####################
        demnCV = 0.16
        days = 2.0
        arrivalHours = 24.0*days
        failure = 20.0
        repair = 2.222222
        ######################
    
        sim_length = 624000.0000000001
    
        def repairTime():
            MTTR = np.random.exponential(repair)
            # print(MTTR)
            return MTTR
    
        def failureTime():
            MTBF = np.random.exponential(failure)
            return MTBF
    
        def periodicDemand():
            global inventoryLevel, shortage, totalDemandArrival, signal, orders, starting_inventory, demandarray
            global running_inventoryLevel, demands12, demandRate, arrivalHours
            # demand = np.floor(np.random.normal(1800, 1800*0.16))
            
            ##########################################
            
            m = 900 # mean of normal distribution
            v = (900*0.2236)**2 # variance of normal distribution
            mu = math.log((m**2)/math.sqrt(v+m**2)) # Mean of lognormal distribution
            sigma = math.sqrt(math.log(v/(m**2)+1)) # Std dev of log normal distribution
            demand = (np.random.lognormal(mu, sigma))

            ##########################################
            
            # demand = 1800.0
            demands12= demand
            # demandarray.append(demand)
            # print(demand)
            totalDemandArrival += 1
            # print "Total Demand Arrival %d " % totalDemandArrival
            # starting_inventory.append(inventoryLevel)
            if inventoryLevel >= demand:
                inventoryLevel = inventoryLevel - demand
                starting_inventory.append(inventoryLevel)
                running_inventoryLevel.append(inventoryLevel)
            else:
                inventoryLevel = 0
                shortage += 1
                starting_inventory.append(inventoryLevel)
                running_inventoryLevel.append(inventoryLevel)
            # print("Inventory level after demand", inventoryLevel)
            
            if inventoryLevel < reorderPoint:
                signal = 1

            demandArrivalFrequency = 24.0
            
            return demand, inventoryLevel, shortage, demandArrivalFrequency, starting_inventory
        
    
        class Machine(object):
            def __init__(self, env):
                self.env = env
                self.parts_made = 0
                self.failure = False
                self.start = 0
                self.repairTime = 0
                self.production = 0
                self.prd = 0
                self.idleTime = False
                self.inventoryLevel = inventoryLevel
                self.processTime = sim_length # float(decimal.Decimal(1.0 / JPH))
                self.productionDuration = self.processTime  # Made a change here
                self.weeklyproduction = 0
                self.weeklyDemand = 0
                self.accumulatedInventory = 0
                self.period_length = self.processTime
                self.timeElapsed = 0
                self.productionStartTime = 0
                self.lengthIdleConsumed = 0
                self.waitUntil1 = 0
                self.periodProduction = 0
                self.repair_per_period = 0
                self.failed_at = 0
                self.waiting_length = 0
                self.count = 0
                self.fixed_length_signal = 0
                self.time_count = 0
                self.time_var = 0
                self.extra_time_after_repair = 0
                self.production_start_after_repair = 0
                self.uptime_length_array = []
                self.weekly_inventory = []
                self.time = []
                self.weekly_inventory_cost = []
                self.periodProduction = []
                self.productionend = 0
                self.inhere = 0
                self.periodicproduction = []
                self.pproduction = 0
    
                env.process(self.demandArrivalFrequency())
                self.process = env.process(self.working())
                env.process(self.machine_failure())
                #env.process(self.weeklyInventory())
                env.process(self.fixedTimeLength())
                env.process(self.Periodic_Production())
    
            def demandArrivalFrequency(self):
                
                global starting_inventory, nextDemandArrivalTime, tup
                while True:
                    prdDemand = periodicDemand()
                    
                    frequency = prdDemand[3]
                    
                    nextDemandArrivalTime += frequency
                    if self.inhere == 1:
                        self.inhere = 0
                        tup = (self.env.now, prdDemand[0], inventoryLevel)
                        # writer.writerow(tup)
                        tup = ("", "", "")
                    else:
                        tup = (self.env.now, prdDemand[0], inventoryLevel)
                    # print(tup)
                    
                    self.weeklyDemand += prdDemand[0]
                    #print("Demand Time", self.env.now)
                    yield self.env.timeout(frequency)
                    self.time_var += frequency
                    
                    
                    if self.time_var >= 480.0:
                        #print(prdDemand[4], len(prdDemand[4]))
                        self.weekly_inventory.append(np.mean(prdDemand[4]))
                        self.weekly_inventory_cost.append(np.mean(prdDemand[4])*inventoryCost)
                        # print(prdDemand[4])
                        starting_inventory = []
                        self.time_var = 0
    
            def working(self):
                global inventoryLevel, signal, orders, totalIdleTime, variableRepairTime
                while True:
                    self.lengthIdleConsumed = self.lengthIdleConsumed
                    i = 0
                    
                    self.productionStartTime = self.env.now
                    #orders += 1
                    while i < 1:
                        self.productionDuration = self.period_length = self.processTime
                        self.waitUntil = 0
                        # print self.waitUntil
                        while self.productionDuration:
                            try:
                                self.start = self.env.now
                                yield self.env.timeout(self.productionDuration)
                                self.productionDuration = 0
                                # print self.env.now
                            except sim.Interrupt:
                                self.failure = True
                                self.failed_at = self.env.now
                                # print("Failed At", self.failed_at)
                                self.productionDuration -= self.env.now - self.start
                                variableRepairTime = repairTime()
                                self.repairTime = variableRepairTime
                                self.repair_per_period += self.repairTime
                                # print("Self Repair Per Period", self.repair_per_period)
                                yield self.env.timeout(self.repairTime)
                                # print("Repair end", self.env.now)
                                self.failure = False
    
            def machine_failure(self):
                """Fails the machine at exponential intervals"""
                global totalIdleTime, signal, variableRepairTime
                while True:
                    failuretime = failureTime()
                    yield self.env.timeout(failuretime)
                    if variableRepairTime > 0:
                        yield self.env.timeout(variableRepairTime)
                        variableRepairTime = 0
                    if not self.failure:
                        if not self.idleTime:
                            self.process.interrupt()

    
            def fixedTimeLength(self):
                global inventoryLevel, signal, orders, totalIdleTime, global_uptime_array
                global nextDemandArrivalTime, tup, running_inventoryLevel
                while True:
                    # print(self.env.now, self.productionStartTime, self.lengthIdleConsumed)
                    
                    if self.lengthIdleConsumed > 0 and self.failure:
                        yield self.env.timeout(self.failed_at + self.repairTime - self.env.now)
                        # print(self.env.now)
                    
                    startOfProduction = self.env.now
                    self.productionStartTime = self.env.now
                    # print(self.env.now, self.productionStartTime)
                    yieldTime = float(decimal.Decimal(leadTime - self.extra_time_after_repair + 0.0000000001))
                    # print(yieldTime)
                    yield self.env.timeout(yieldTime) # - (self.productionStartTime - self.env.now)
                    #print("Production End Time", self.env.now)
                    self.extra_time_after_repair = 0.0
                    # print(self.env.now, self.failure)
                    
                    if self.failure:
                        orders += 1
                        #print(self.failed_at, self.repairTime)
                        
                        self.production = np.floor((self.env.now - self.productionStartTime \
                                                    - (self.repair_per_period - (self.failed_at + self.repairTime - self.env.now)))*JPH)
                        
                        # print(self.production/JPH)
                        self.pproduction = self.production
                        self.periodProduction.append(self.production)
                        
                        """self.env.now - self.productionStartTime - self.lengthIdleConsumed 
                        provides the max. available length for production. Next, reduce the repair lengths"""
                        
                        """self.env.now - self.failed_at provides the repair time consumed in current period"""
                        """self.repair_per_period total repair time in this current period"""
                        
                        #print("Production ending in failure", self.production)
                        
                        self.repair_per_period = 0

                        """self.repair_per_period here computes the time consumed from the next period"""
                        # self.processTime = leadTime - self.repair_per_period
                        self.productionStartTime = self.failed_at + self.repairTime
                        self.production_start_after_repair = self.failed_at + self.repairTime
                    
                    else:
                        orders += 1
                        self.production = np.floor((self.env.now - self.productionStartTime - self.repair_per_period)*JPH)
                        #print("Production no failure", self.production)
                        # print(self.production/JPH)
                        self.pproduction = self.production
                        self.periodProduction.append(self.production)
                        self.repair_per_period = 0.0
                        # self.processTime = leadTime - self.repair_per_period
                        self.productionStartTime = self.env.now + self.repair_per_period
                    

                    self.productionend = self.env.now
                    self.prd += self.production

                    inventoryLevel += self.production
                    starting_inventory.append(inventoryLevel)
                    running_inventoryLevel.append(inventoryLevel)

                    global_uptime_array.append(self.production)
                    
                    tupii = tup + (startOfProduction, self.production, self.productionend, self.productionend - startOfProduction, inventoryLevel, self.production*24.0/(self.productionend - startOfProduction))
                    tup = ("", "", "")

                    self.weeklyproduction += self.production
                    self.lengthIdleConsumed = 0
                    
                    if inventoryLevel <= reorderPoint:
                        signal = 1
                        # print("Start of production", self.env.now)
                        self.time.append(0.00)
                    else:
                        start = self.env.now                                                
                        # print(inventoryLevel, inventoryLevel-reorderPoint)
                        while inventoryLevel > reorderPoint:
                            self.inhere = 1
                            # print(self.inhere, self.env.now)
                            self.idleTime = True
                            yield self.env.timeout(nextDemandArrivalTime - self.env.now)
                            # yield self.env.timeout(0.5)
                            self.idleTime = False
                            self.inhere = 0
                                
                            end = self.env.now
                            self.lengthIdleConsumed = end-start
                            "In follwoing line CONSUMED is the length of idle time"
                            consumed = end
                            #print(self.lengthIdleConsumed)
                        
                        self.time.append(end-start)
                        # print("Start of production", self.env.now)
                        tupi = tup + ("", "", "", "", "", "") + (end-start, )                       
                        
                        
                        if self.production_start_after_repair >= consumed:
                            self.extra_time_after_repair = (self.production_start_after_repair - consumed)
                            self.idleTime = True
                            yield self.env.timeout(self.extra_time_after_repair)
                            self.idleTime = False
                            self.extra_time_after_repair = self.lengthIdleConsumed + (self.production_start_after_repair - consumed)
                            
                            while self.extra_time_after_repair > leadTime:
                                self.extra_time_after_repair = self.extra_time_after_repair - leadTime
                            
                            # print(self.production_start_after_repair, consumed, self.extra_time_after_repair, leadTime)
                            self.lengthIdleConsumed = 0
                            
                            """Yield here so that repair length, which is greater than idle time, is consumed """
                        else:
                            self.production_start_after_repair = 0
                        
                        
                        tup = ("", "", "")
                        # print(tupi)
                        self.fixed_length_signal = self.env.now

                        totalIdleTime += self.lengthIdleConsumed
            
            def Periodic_Production(self):
                global demandarray, demands12
                while True:
                    yield self.env.timeout(1200.0)
                    self.periodicproduction.append(self.pproduction)
                    self.pproduction = 0
                    
                    demandarray.append(demands12)
                    demands12 = 0
                    # print(demandarray)
                    
        env = sim.Environment()
        machines = Machine(env)
        env.run(until=sim_length)
        
        
        var_uptime_length = np.var(global_uptime_array)
        average_uptime_length = np.mean(global_uptime_array)
        
        totalPenaltyCost = shortage*penaltyCost
        totalOrderingCost = orders*fixedCost
        totalInventoryCost = np.sum(machines.weekly_inventory_cost)
    
        serviceLevel = 1.0 - float(decimal.Decimal(shortage)/decimal.Decimal(totalDemandArrival))
    
        tCC += (totalPenaltyCost + totalOrderingCost + totalInventoryCost)
        tCC_array.append(totalPenaltyCost + totalOrderingCost + totalInventoryCost)
        
        avgInventory.append(np.mean(machines.weekly_inventory))
        avgOrder.append(orders)
        avgLostSales.append(shortage)
        
        Pcost += totalPenaltyCost
        Ocost += totalOrderingCost
        Icost += totalInventoryCost
        avgServiceLevel += serviceLevel
        nrep += 1
        totalUnitsProduced += machines.prd
        Tidletime += totalIdleTime
        
        avgServiceLevel_array.append(serviceLevel)
    
    tCC = np.mean(tCC_array)
    avgServiceLevel = avgServiceLevel/rep
    Pcost = Pcost/rep
    Icost = Icost/rep
    Ocost = Ocost/rep
    Tidletime = Tidletime/rep
    totalUnitsProduced = totalUnitsProduced/rep
    
    var_uptime_length = np.var(global_uptime_array)
    average_uptime_length = np.mean(global_uptime_array)
    
    meanServiceLevel = np.mean(avgServiceLevel_array)

    print("Total Cost", tCC, meanServiceLevel)

    return tCC, meanServiceLevel


def Poolfunction(reOrderPoint, leadtime):
    QRCode = RunQRcode(reOrderPoint, leadtime)
    return QRCode
