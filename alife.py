# -*- coding: utf-8 -*-
"""ALife.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MP1MFpJ-4gHOWln-tzZa0spxfNmxIcZ5

Key aspects of this artificial cell model:

Motivators (Fitness Functions):

Energy maintenance
Survival time
Successful divisions
Resource efficiency


Parameters:

Internal:

Energy level
Age
Metabolism rate
Division threshold


Environmental:

Nutrient availability
Temperature
Chemical gradients




Key Behaviors:

Metabolism (energy production/consumption)
Homeostasis (internal balance)
Movement (environment exploration)
Resource uptake
Cell division
Waste management


Learning Mechanisms:

Reinforcement learning for action selection
Adaptive metabolism based on environment
Homeostatic feedback loops



To create a more complex simulation, we could add:

Membrane Properties:

pythonCopymembrane_permeability = layers.Dense(
    units=num_chemicals,
    activation='sigmoid',
    name='membrane_controller'
)

DNA/RNA-like Information Storage:

pythonCopyclass GeneticInformation(layers.Layer):
    def __init__(self):
        self.gene_sequence = tf.Variable(
            initial_value=tf.random.normal([gene_length]),
            trainable=True
        )

Chemical Reaction Networks:

pythonCopyclass MetabolicNetwork(layers.Layer):
    def __init__(self):
        self.reaction_rates = layers.Dense(
            units=num_reactions,
            activation='softplus'
        )
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class ArtificialCell(keras.Model):
    def __init__(self):
        super(ArtificialCell, self).__init__()

        # Constants
        self.ENERGY_THRESHOLD = 0.7  # Energy level needed for division
        self.METABOLISM_RATE = 0.1   # Base rate of energy consumption

        # Internal state trackers
        self.energy_level = tf.Variable(1.0)
        self.age = tf.Variable(0.0)
        self.survival_time = tf.Variable(0.0)

        # Neural Networks for different cell functions
        self.metabolism_network = self._build_metabolism_network()
        self.homeostasis_network = self._build_homeostasis_network()
        self.action_network = self._build_action_network()

    def _build_metabolism_network(self):
        inputs = keras.Input(shape=(4,))  # nutrients, temp, chemicals, current_energy
        x = layers.Dense(16, activation='relu')(inputs)
        x = layers.Dense(8, activation='relu')(x)
        outputs = layers.Dense(1, activation='sigmoid')(x)  # Energy production rate
        return keras.Model(inputs=inputs, outputs=outputs)

    def _build_homeostasis_network(self):
        inputs = keras.Input(shape=(6,))  # internal_state + environmental_conditions
        x = layers.Dense(32, activation='relu')(inputs)
        x = layers.Dense(16, activation='relu')(x)
        outputs = layers.Dense(3, activation='sigmoid')(x)  # homeostatic_responses
        return keras.Model(inputs=inputs, outputs=outputs)

    def _build_action_network(self):
        inputs = keras.Input(shape=(7,))  # internal_state + metabolism + homeostasis
        x = layers.Dense(32, activation='relu')(inputs)
        x = layers.Dense(16, activation='relu')(x)
        outputs = layers.Dense(4, activation='softmax')(x)  # movement, uptake, excretion, division
        return keras.Model(inputs=inputs, outputs=outputs)

    def simulate_step(self, environment_state):
        # Unpack environment state
        nutrients, temperature, chemicals = environment_state

        # Calculate metabolism
        metabolism_input = tf.concat([
            nutrients,
            [temperature],
            chemicals,
            [self.energy_level]
        ], axis=0)
        energy_delta = self.metabolism_network(tf.expand_dims(metabolism_input, 0))

        # Update energy level
        self.energy_level.assign(
            tf.clip_by_value(
                self.energy_level + energy_delta - self.METABOLISM_RATE,
                0.0, 1.0
            )
        )

        # Calculate homeostasis response
        homeostasis_input = tf.concat([
            [self.energy_level],
            [temperature],
            chemicals,
            [self.age],
            [self.survival_time]
        ], axis=0)
        homeostasis_response = self.homeostasis_network(tf.expand_dims(homeostasis_input, 0))

        # Decide actions
        action_input = tf.concat([
            [self.energy_level],
            [self.age],
            homeostasis_response[0],
            energy_delta[0],
            [self.survival_time]
        ], axis=0)
        actions = self.action_network(tf.expand_dims(action_input, 0))

        # Update internal state
        self.age.assign_add(1.0)
        self.survival_time.assign_add(1.0)

        # Return actions and current state
        return {
            'actions': actions[0].numpy(),
            'energy_level': self.energy_level.numpy(),
            'age': self.age.numpy(),
            'survival_time': self.survival_time.numpy()
        }

    def should_divide(self):
        return self.energy_level > self.ENERGY_THRESHOLD and self.age > 100

    def divide(self):
        # Create new cell with half energy
        new_cell = ArtificialCell()
        new_cell.energy_level.assign(self.energy_level / 2)
        self.energy_level.assign(self.energy_level / 2)
        self.age.assign(0.0)
        return new_cell

# Fitness function to evaluate cell performance
def calculate_fitness(cell_state):
    return (cell_state['survival_time'] * cell_state['energy_level']) / 100.0

