#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonctions de statistiques
^^^^^^^^^^^^^^^^^^^^^^^^^

Created on Tue Nov 24 12:32:10 2020

@author: Cyrile Delestre
"""

from typing import Optional

import numpy as np

def weighted_avg_and_std(x: np.ndarray,
                         sample_weight: Optional[np.ndarray]=None,
                         axis: Optional[int]=None):
    """
    Retourne la moyenne de l'écart-type avec un poids sur chaque mesure.
    
    Parameters
    ----------
    x : np.ndarray
        variable aléatoire.
    sample_weight : Optional[np.ndarray] (=None)
        poids sur les samples. Doit avoir la même dimension que x un vecteur
        colonne.
    axis : Optional[int] (=None)
        dimension de l'opération. Si None f^ait sur toutes les dimensions.

    Returns
    -------
    mean : Union[np.ndarray, float]
        moyenne pondérée, scalaire si axis = None, sinon 
        (n1 x ... x ni x ... nq) si axis = i
    std : Union[np.ndarray, float]
        écart-type pondéré, scalaire si axis = None, sinon 
        (n1 x ... x ni x ... nq) si axis = i

    Notes
    -----
    Cette fonction retourne également la moyenne car elle en as besoin pour 
    le calcul de la variance. Il s'agit également de la moyenne pondérée.
    """
    mean = np.average(
        a=x,
        weights=sample_weight,
        axis=axis
    )
    var = np.average(
        a=(x-mean)**2,
        weights=sample_weight,
        axis=axis
    )
    if axis:
        # Obligé de faire un reshape sinon la sortie peut ne pas préserver les 
        # dimensions.
        ind_reshape = list(x.shape)
        ind_reshape[axis] = 1
        return mean.reshape(*ind_reshape), np.sqrt(var).reshape(*ind_reshape)
    return mean, np.sqrt(var)
