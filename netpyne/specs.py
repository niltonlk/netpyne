"""
specs.py
NetParams is a class containing a set of network parameters using a standardized structure
SimConfig is a class containing a set of simulation configurations using a standardized structure
Contributors: salvadordura@gmail.com
"""

from collections import OrderedDict
from netpyne import utils

###############################################################################
# Dict class (allows dot notation for dicts)
###############################################################################

class Dict(dict):

    __slots__ = []


    def __init__(*args, **kwargs):
        self = args[0]
        args = args[1:]
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if args:
            self.update(self.dotify(args[0]))
        if len(kwargs):
            self.update(self.dotify(kwargs))

    # only called if k not found in normal places
    def __getattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)


    def todict(self):
        return self.undotify(self)

    def fromdict(self, d):
        d = self.dotify(d)
        for k,v in d.iteritems():
            self[k] = v

    def __repr__(self):
        keys = self.keys()
        args = ', '.join(['%s: %r' % (key, self[key]) for key in keys])
        return '{%s}' % (args)


    def dotify(self, x):
        if isinstance(x, dict):
            return Dict( (k, self.dotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, (list, tuple)):
            return type(x)( self.dotify(v) for v in x )
        else:
            return x

    def undotify(self, x):
        if isinstance(x, dict):
            return dict( (k, self.undotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, (list, tuple)):
            return type(x)( self.undotify(v) for v in x )
        else:
            return x

    def __rename__(self, old, new, label=None):
        '''
        old (string): old dict key
        new (string): new dict key
        label (list/tuple of strings): nested keys pointing to dict with key to be replaced; 
            e.g. ('PYR', 'secs'); use None to replace root key; defaults to None 
        
        returns: True if successful, False otherwse
        '''
        obj = self
        if isinstance(label, (tuple, list)):
            for ip in range(len(label)):
                try:
                    obj = obj[label[ip]] 
                except:
                    return False 

        if old in obj:
            obj[new] = obj.pop(old)  # replace
            return True
        else:
            return False

    def rename(self, *args, **kwargs):
        self.__rename__(*args, **kwargs)

    def __missing__(self, key):
        if key and not key.startswith('_ipython'):
            value = self[key] = Dict()
            return value

    def __getstate__ (self):
        return self.todict()

    def __setstate__ (self, d):
        self = self.fromdict(d)


###############################################################################
# ODict class (allows dot notation for ordered dicts)
###############################################################################

class ODict(OrderedDict):

    __slots__ = []

    def __init__(self, *args, **kwargs):
        super(ODict, self).__init__(*args, **kwargs)

    def __contains__(self, k):
        try:
            return hasattr(self, k) or dict.__contains__(self, k)
        except:
            return False

    # only called if k not found in normal places
    def __getattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            return super(ODict, self).__getattr__(k)
        except AttributeError:
            try:
                return super(ODict, self).__getitem__(k)
            except KeyError:
                raise AttributeError(k)


    def __setattr__(self, k, v):
        if k.startswith('_OrderedDict'):
            super(ODict, self).__setattr__(k,v)
        else:
            try:
                super(ODict, self).__setitem__(k,v)
            except:
                raise AttributeError(k)


    def __getitem__(self, k):
        return super(ODict, self).__getitem__(k)


    def __setitem__(self, k, v):
        super(ODict, self).__setitem__(k,v)

    def __delattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                super(ODict, self).__delattr__(k)
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def toOrderedDict(self):
        return self.undotify(self)

    def fromOrderedDict(self, d):
        d = self.dotify(d)
        for k,v in d.iteritems():
            self[k] = v

    def __repr__(self):
        keys = self.keys()
        args = ', '.join(['%s: %r' % (key, self[key]) for key in keys])
        return '{%s}' % (args)


    def dotify(self, x):
        if isinstance(x, OrderedDict):
            return ODict( (k, self.dotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, dict):
            return Dict( (k, self.dotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, (list, tuple)):
            return type(x)( self.dotify(v) for v in x )
        else:
            return x

    def undotify(self, x):
        if isinstance(x, OrderedDict):
            return OrderedDict( (k, self.undotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, dict):
            return dict( (k, self.undotify(v)) for k,v in x.iteritems() )
        elif isinstance(x, (list, tuple)):
            return type(x)( self.undotify(v) for v in x )
        else:
            return x

    def __rename__(self, old, new, label=None):
        '''
        old (string): old dict key
        new (string): new dict key
        label (list/tuple of strings): nested keys pointing to dict with key to be replaced; 
            e.g. ('PYR', 'secs'); use None to replace root key; defaults to None 
        
        returns: True if successful, False otherwse
        '''
        obj = self
        if isinstance(label, (tuple, list)):
            for ip in range(len(label)):
                try:
                    obj = obj[label[ip]] 
                except:
                    return False 

        if old in obj:
            obj[new] = obj.pop(old)  # replace
            return True
        else:
            return False

    def rename(self, *args, **kwargs):
        self.__rename__(*args, **kwargs)
        
    def __getstate__ (self):
        return self.toOrderedDict()

    def __setstate__ (self, d):
        self = self.fromOrderedDict(d)


class PopParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False
        
        dimParams = ['numCells', 'density', 'gridSpacing']
        if param in dimParams:
            for removeParam in dimParams: d.pop(removeParam, None)  # remove other properties

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)
    
class CellParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        success = self.__rename__(old, new, label)

        try:
            # special case: renaming cellParams[x]['secs'] requires updating topology
            if isinstance(label, (list, tuple)) and 'secs' in self[label[0]]:
                d = self[label[0]]
                for sec in d['secs'].values():  # replace appearences in topol
                    if sec['topol'].get('parentSec') == old: 
                        sec['topol']['parentSec'] = new
            return success
        except:
            return False


class ConnParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)


class SynMechParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)


class SubConnParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)


class StimSourceParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)


class StimTargetParams (ODict):
    def setParam(self, label, param, value):
        if label in self: 
            d = self[label]
        else:
            return False

        d[param] = value

        return True

    def rename(self, old, new, label=None):
        return self.__rename__(old, new, label)


###############################################################################
# NETWORK PARAMETERS CLASS
###############################################################################

class NetParams (object):

    def __init__(self, netParamsDict=None):
        self._labelid = 0
        # General network parameters
        self.scale = 1   # scale factor for number of cells
        self.sizeX = 100 # x-dimension (horizontal length) size in um
        self.sizeY = 100 # y-dimension (vertical height or cortical depth) size in um
        self.sizeZ = 100 # z-dimension (horizontal depth) size in um
        self.shape = 'cuboid' # network shape ('cuboid', 'cylinder' or 'ellipsoid')


        ## General connectivity parameters
        self.scaleConnWeight = 1 # Connection weight scale factor (NetStims not included)
        self.scaleConnWeightNetStims = 1 # Connection weight scale factor for NetStims
        self.scaleConnWeightModels = {} # Connection weight scale factor for each cell model eg. {'Izhi2007': 0.1, 'Friesen': 0.02}
        self.defaultWeight = 1  # default connection weight
        self.defaultDelay = 1  # default connection delay (ms)
        self.defaultThreshold = 10  # default Netcon threshold (mV)
        self.propVelocity = 500.0  # propagation velocity (um/ms)

        # Cell params dict
        self.cellParams = CellParams()

        # Population params dict
        self.popParams = PopParams()  # create list of populations - each item will contain dict with pop params
        self.popTagsCopiedToCells = ['cellModel', 'cellType']

        # Synaptic mechanism params dict
        self.synMechParams = SynMechParams()

        # Connectivity params dict
        self.connParams = ConnParams()

        # Subcellular connectivity params dict
        self.subConnParams = SubConnParams()

        # Stimulation source and target params dicts
        self.stimSourceParams = StimSourceParams()
        self.stimTargetParams = StimTargetParams()

        # fill in params from dict passed as argument
        if netParamsDict:
            for k,v in netParamsDict.iteritems():
                if isinstance(v, OrderedDict):
                    setattr(self, k, ODict(v))
                elif isinstance(v, dict):
                    setattr(self, k, Dict(v))
                else:
                    setattr(self, k, v)

    def save(self, filename):
        import os
        basename = os.path.basename(filename)
        folder = filename.split(basename)[0]
        ext = basename.split('.')[1]

        # make dir
        try:
            os.mkdir(folder)
        except OSError:
            if not os.path.exists(folder):
                print ' Could not create', folder

        dataSave = {'net': {'params': self.__dict__}}

        # Save to json file
        if ext == 'json':
            import json
            print('Saving netParams to %s ... ' % (filename))
            with open(filename, 'w') as fileObj:
                json.dump(dataSave, fileObj, indent=4, sort_keys=True)


    def addCellParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.cellParams[label] = Dict(params)

    def addPopParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.popParams[label] = Dict(params)

    def addSynMechParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.synMechParams[label] = Dict(params)

    def addConnParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.connParams[label] = Dict(params)

    def addSubConnParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.subConnParams[label] = Dict(params)

    def addStimSourceParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.stimSourceParams[label] = Dict(params)

    def addStimTargetParams(self, label=None, params=None):
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        self.stimTargetParams[label] = Dict(params)

    # def rename(self, attr, old, new):
    #     try:
    #         obj = getattr(self, attr)
    #     except:
    #         print 'Error renaming: netParams does not contain %s' % (attr)
    #         return False

    #     if old not in obj:
    #         print 'Error renaming: netParams.%s rule does not contain %s' % (attribute, old)
    #         return False

    #     obj[new] = obj.pop(old)  # replace

    #     return True


    def importCellParams(self, label, conds, fileName, cellName, cellArgs=None, importSynMechs=False, somaAtOrigin=False, cellInstance=False):
        if cellArgs is None: cellArgs = {}
        if not label:
            label = int(self._labelid)
            self._labelid += 1
        secs, secLists, synMechs, globs = utils.importCell(fileName, cellName, cellArgs, cellInstance)
        cellRule = {'conds': conds, 'secs': secs, 'secLists': secLists, 'globals': globs}

        # adjust cell 3d points so that soma is at location 0,0,0
        if somaAtOrigin:
            somaSec = next((sec for sec in cellRule['secs'] if 'soma' in sec), None)
            if not somaSec or not 'pt3d' in cellRule['secs'][somaSec]['geom']:
                print 'Warning: cannot place soma at origin because soma does not exist or does not contain pt3d'
                return
            soma3d = cellRule['secs'][somaSec]['geom']['pt3d']
            midpoint = int(len(soma3d)/2)
            somaX, somaY, somaZ = soma3d[midpoint][0:3]
            for sec in cellRule['secs'].values():
                for i,pt3d in enumerate(sec['geom']['pt3d']):
                    sec['geom']['pt3d'][i] = (pt3d[0] - somaX, pt3d[1] - somaY, pt3d[2] - somaZ, pt3d[3])

        self.addCellParams(label, cellRule)

        if importSynMechs:
            for synMech in synMechs: self.addSynMechParams(cellName+'_'+synMech.pop('label'), synMech)

        return self.cellParams[label]

    def importCellParamsFromNet(self, labelList, condsList, fileName, cellNameList, importSynMechs=False):
        utils.importCellsFromNet(self, fileName, labelList, condsList, cellNameList, importSynMechs)
        return self.cellParams


    def addCellParamsSecList(self, label, secListName, somaDist=None, somaDistY=None):
        import numpy as np

        if label in self.cellParams:
            cellRule = self.cellParams[label]
        else:
            print 'Error adding secList: netParams.cellParams does not contain %s' % (label)
            return

        if somaDist is not None and (not isinstance(somaDist, list) or len(somaDist) != 2):
            print 'Error adding secList: somaDist should be a list with 2 elements'
            return

        if somaDistY is not None and (not isinstance(somaDistY, list) or len(somaDistY) != 2):
            print 'Error adding secList: somaDistY should be a list with 2 elements'
            return


        secList = []
        for secName, sec in cellRule.secs.iteritems():
            if 'pt3d' in sec['geom']:
                pt3d = sec['geom']['pt3d']
                midpoint = int(len(pt3d)/2)
                x,y,z = pt3d[midpoint][0:3]
                if somaDist:
                    distSec = np.linalg.norm(np.array([x,y,z]))
                    if distSec >= somaDist[0] and distSec <= somaDist[1]:
                        secList.append(secName)
                elif somaDistY:
                    if y >= somaDistY[0] and y <= somaDistY[1]:
                        secList.append(secName)                    

            else:
                print 'Error adding secList: Sections do not contain 3d points'
                return

        cellRule.secLists[secListName] = list(secList)

    def swapCellParamsPt3d(self, label, origIndex, targetIndex):
        if label in self.cellParams:
            cellRule = self.cellParams[label]
        else:
            print 'Error swapping 3d pts: netParams.cellParams does not contain %s' % (label)
            return

        if origIndex not in range(4) and targetIndex not in range(4): # check valid indices (x,y,z,d)
            print 'Error swapping 3d pts: indices should be 0, 1, 2 or 3 (x,y,z,d)'
            return

        for sec in cellRule.secs.values():
            if 'pt3d' in sec['geom']:
                pt3d = sec['geom']['pt3d']
                for i,pt in enumerate(pt3d): pt3d[i] = list(pt)
                for pt in pt3d:
                    tmp = float(pt[origIndex])
                    pt[origIndex] = float(pt[targetIndex])
                    pt[targetIndex] = tmp


    def renameCellParamsSec(self, label, oldSec, newSec):
        self.cellParams.rename(oldSec, newSec, (label, 'secs'))


    def addCellParamsWeightNorm(self, label, fileName, threshold=1000):
        import pickle
        if label in self.cellParams:
            cellRule = self.cellParams[label]
        else:
            print 'Error adding weightNorm: netParams.cellParams does not contain %s' % (label)
            return

        with open(fileName, 'r') as fileObj:
            weightNorm = pickle.load(fileObj)

        try:
            somaSec = next((k for k in weightNorm.keys() if k.startswith('soma')),None)
            somaWeightNorm = weightNorm[somaSec][0]
        except:
            print 'Error setting weightNorm: no soma section available to set threshold'
            return
        for sec, wnorm in weightNorm.iteritems():
            if sec in cellRule['secs']:
                wnorm = [min(wn,threshold*somaWeightNorm) for wn in wnorm]
                cellRule['secs'][sec]['weightNorm'] = wnorm  # add weight normalization factors for each section


    def saveCellParamsRule(self, label, fileName):
        import pickle, json, os

        ext = os.path.basename(fileName).split('.')[1]

        if label in self.cellParams:
            cellRule = self.cellParams[label]
        else:
            print 'Error saving: netParams.cellParams does not contain %s' % (label)
            return

        if ext == 'pkl':
            with open(fileName, 'w') as fileObj:
                pickle.dump(cellRule, fileObj)
        elif ext == 'json':
            with open(fileName, 'w') as fileObj:
                cellRule = json.dump(cellRule, fileObj)


    def loadCellParamsRule(self, label, fileName):
        import pickle, json, os

        ext = os.path.basename(fileName).split('.')[1]
        if ext == 'pkl':
            with open(fileName, 'r') as fileObj:
                cellRule = pickle.load(fileObj)
        elif ext == 'json':
            with open(fileName, 'r') as fileObj:
                cellRule = json.load(fileObj)
        
        self.cellParams[label] = cellRule


    def todict(self):
        from sim import replaceDictODict
        return replaceDictODict(self.__dict__)


###############################################################################
# SIMULATION CONFIGURATION CLASS
###############################################################################

class SimConfig (object):

    def __init__(self, simConfigDict = None):
        # Simulation parameters
        self.duration = self.tstop = 1*1e3 # Duration of the simulation, in ms
        self.dt = 0.025 # Internal integration timestep to use
        self.hParams = Dict({'celsius': 6.3, 'v_init': -65.0, 'clamp_resist': 0.001})  # parameters of h module
        self.cache_efficient = False  # use CVode cache_efficient option to optimize load when running on many cores
        self.cvode_active = False  # Use CVode variable time step
        self.cvode_atol = 0.001  # absolute error tolerance
        self.seeds = Dict({'conn': 1, 'stim': 1, 'loc': 1}) # Seeds for randomizers (connectivity, input stimulation and cell locations)
        self.rand123GlobalIndex = None  # Sets the global index used by all instances of the Random123 instances of Random
        self.createNEURONObj = True  #  create runnable network in NEURON when instantiating netpyne network metadata
        self.createPyStruct = True  # create Python structure (simulator-independent) when instantiating network
        self.addSynMechs = True  # whether to add synaptich mechanisms or not
        self.includeParamsLabel = True  # include label of param rule that created that cell, conn or stim
        self.gatherOnlySimData = False  # omits gathering of net+cell data thus reducing gatherData time
        self.compactConnFormat = False  # replace dict format with compact list format for conns (need to provide list of keys to include)
        self.saveCellSecs = True  # save all the sections info for each cell (False reduces time+space; available in netParams; prevents re-simulation)
        self.saveCellConns = True  # save all the conns info for each cell (False reduces time+space; prevents re-simulation)
        self.timing = True  # show timing of each process
        self.saveTiming = False  # save timing data to pickle file
        self.printRunTime = False  # print run time at interval (in sec) specified here (eg. 0.1)
        self.printPopAvgRates = False  # print population avg firing rates after run
        self.verbose = False  # show detailed messages

        # Recording
        self.recordCells = []  # what cells to record from (eg. 'all', 5, or 'PYR')
        self.recordTraces = {}  # Dict of traces to record
        self.recordStim = False  # record spikes of cell stims
        self.recordLFP = [] # list of 3D locations to record LFP from
        self.saveLFPCells = False  # Store LFP generate individually by each cell 
        self.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)
        self.recordTime = True  # record time step of recording

        # Saving
        self.simLabel = ''  # name of simulation (used as filename if none provided)
        self.saveFolder = ''  # path where to save output data
        self.filename = 'model_output'  # Name of file to save model output (if omitted then saveFolder+simLabel is used)
        self.saveDataInclude = ['netParams', 'netCells', 'netPops', 'simConfig', 'simData']
        self.timestampFilename = False  # Add timestamp to filename to avoid overwriting
        self.savePickle = False # save to pickle file
        self.saveJson = False # save to json file
        self.saveMat = False # save to mat file
        self.saveCSV = False # save to txt file
        self.saveDpk = False # save to .dpk pickled file
        self.saveHDF5 = False # save to HDF5 file
        self.saveDat = False # save traces to .dat file(s)
        self.backupCfgFile = [] # copy cfg file, list with [sourceFile,destFolder] (eg. ['cfg.py', 'backupcfg/'])

        # error checking
        self.checkErrors = False # whether to validate the input parameters (will be turned off if num processors > 1)
        self.checkErrorsVerbose = False # whether to print detailed errors during input parameter validation
        # self.exitOnError = False # whether to hard exit on error

        # Analysis and plotting
        self.analysis = ODict()

        # fill in params from dict passed as argument
        if simConfigDict:
            for k,v in simConfigDict.iteritems():
                if isinstance(v, OrderedDict):
                    setattr(self, k, ODict(v))
                elif isinstance(v, dict):
                    setattr(self, k, Dict(v))
                else:
                    setattr(self, k, v)

    def save(self, filename):
        import os
        basename = os.path.basename(filename)
        folder = filename.split(basename)[0]
        ext = basename.split('.')[1]

        # make dir
        try:
            os.mkdir(folder)
        except OSError:
            if not os.path.exists(folder):
                print ' Could not create', folder

        dataSave = {'simConfig': self.__dict__}

        # Save to json file
        if ext == 'json':
            import json
            print('Saving simConfig to %s ... ' % (filename))
            with open(filename, 'w') as fileObj:
                json.dump(dataSave, fileObj, indent=4, sort_keys=True)

    def addAnalysis(self, func, params):
        self.analysis[func] =  params

    def todict(self):
        from sim import replaceDictODict
        return replaceDictODict(self.__dict__)
