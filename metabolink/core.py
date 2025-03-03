from pytfa.redgem.lumpgem import LumpGEM
from pytfa.io.json import load_json_model
import numpy as np 

from cobra import Reaction


EPSILON = 1e-6

# LumpGEM parameters
DEFAULT_PARAMETERS = {
    'core_subsystems': [],
    'extracellular_system': [],
    'timeout': 3600,  # max time in s
    "constraint_method": 'integer',  # 'integer' or 'continuous'
    # Stuff we dont need for this purpose
    "small_metabolites": [],
    "cofactor_pairs": [],
    "inorganics": [],
    "max_lumps_per_BBB": 100  # Maximal number of alternatives
}

def find_lumps(metabolite_sink, model, params=DEFAULT_PARAMETERS, 
                core_reactions=[], method='min',):  
        # Lump the reactions 
        
        params['growth_rate'] = 1.0
        params['biomass_rxns'] =  [metabolite_sink,]

        resp_model = model.copy()
        
        #LumpGEM needs to take as list of core reaction id as input
        subnetwork_extraction = LumpGEM(resp_model, core_reactions, params, min_exchange=True, bigM=200 )
        lumps = subnetwork_extraction.compute_lumps(force_solve=False, method=method)

        return lumps


def find_precursor_sets(metabolite_id, model, params=DEFAULT_PARAMETERS, defined_precursors=None, method='min'):   

    if defined_precursors is None:
        core_reactions = [r.id for r in model.reactions if not r in model.boundary]
    else:
        core_reactions = [r.id for r in model.reactions if not r.id in defined_precursors]

    # Add a sink for the metabolite
    if np.isscalar(metabolite_id):
        met = model.metabolites.get_by_id(metabolite_id)
        try:
            r = model.add_boundary(met, type='sink', lb=0, ub=1000)
        except ValueError:
            raise NotImplementedError("Boundary already exsists not sure what todo ... ") # Boundary already exists
        
        # Test if the metabolite can be produced
        model.objective = r
        solution = model.optimize()
        if solution.objective_value < EPSILON:
            raise ValueError("Metabolite cannot be produced")
        else:
            print(f"Metabolite {metabolite_id} can be produced {solution.objective_value}")

    else:
        # TODO implement multiple metabolites a list of metabolite ids and make a pseudo biomass reaction

        # Create a pseudo biomass reaction
        r = Reaction('pseudo_biomass')

        # Add the metabolites to the reaction
        r.add_metabolites({model.metabolites.get_by_id(met_id): -1 for met_id in metabolite_id})

        # Add the reaction to the model
        model.add_reactions([r,])

        # Test if all the metabolites can be produced
        model.objective = r
        solution = model.optimize()
        if solution.objective_value < EPSILON:
            # Remove the sink/biomass reaction
            model.remove_reactions([r])
            raise ValueError("Metabolites cannot be produced")
        else:
            print(f"Metabolites {metabolite_id} can be simultanously produced {solution.objective_value}") 

    lumps = find_lumps(r.id, model, params=params, core_reactions=core_reactions, method=method)

    # Remove the sink/biomass reaction
    model.remove_reactions([r])

    # TODO process the lumps to generate a list of precursor metabolite sets 
    # lumps dict metabolite id -> lump object 

    precursor_sets = {metabolite.id: [lump.metabolites for lump in met_lumps] for metabolite, met_lumps in lumps.items()}

    return precursor_sets


