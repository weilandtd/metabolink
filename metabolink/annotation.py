#!/usr/bin/env python3
import numpy as np


def find_metabolites_from_annotation(id, model):
    """
    Find metabolites in a model based on a given annotation id

    Parameters
    ----------
    id : str
        The annotation id to search for
    model : cobra.Model
        The model to search in  
        
    """

    # Veryfi if id is a non empty string
    if id and isinstance(id, str):
        metabolites = [] 
        for met in model.metabolites:
            for id_type, ids in met.annotation.items():
                # TODO fix HMDB old vs new
                if id_type == 'hmdb':
                    # Compare only last 5 digits of HMDB ids
                    if id[-5:] in [i[-5:] for i in ids]:
                        metabolites.append(met.id)
                if id in ids:
                    metabolites.append(met.id)
        if metabolites not in [[], None]:            
            return metabolites
        else:
            return None
    else:
        return None