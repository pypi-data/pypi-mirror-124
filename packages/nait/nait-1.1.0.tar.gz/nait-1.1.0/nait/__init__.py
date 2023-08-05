import numpy as np
import time
import math
import os
class standard():
    def train(training_inputs, training_expectations, training_epochs):
        start_time = time.time()
        if isinstance(training_inputs, list) == False:
            raise ValueError(f"{training_inputs} should be type 'list'")
        if isinstance(training_expectations, list) == False:
            raise ValueError(f"{training_expectations} should be type 'list'")
        if isinstance(training_inputs[0], list) == False:
            raise ValueError(f"{training_inputs[0]} should be type 'list'")
        if isinstance(training_expectations[0], list) == False:
            raise ValueError(f"{training_expectations[0]} should be type 'list'")
        if len(training_inputs) != len(training_expectations):
            raise IndexError(f"{training_inputs} should be the same length as {training_expectations}")
        if isinstance(training_inputs[0][0], int) == False and isinstance(training_inputs[0][0], float) == False:
            raise ValueError(f"{training_inputs[0][0]} should be type 'integer' or 'float'")
        if isinstance(training_expectations[0][0], int) == False and isinstance(training_expectations[0][0], float) == False:
            raise ValueError(f"{training_expectations[0][0]} should be type 'integer' or 'float'")
        number_of_inputs = len(training_inputs[0])
        number_of_outputs = len(training_expectations[0])
        version = "1.1.0"
        epoch_size = 1000
        number_of_iterations = epoch_size * training_epochs
        os.system(f'title NAIT {version}')
        init_weights_l1 = [[1/number_of_inputs]*number_of_inputs]*16
        init_weights_l2 = [[1/16]*16]*16
        init_weights_l3 = [[1/16]*16]*number_of_outputs
        init_biases_l1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l3 = [0]*number_of_outputs
        weights_l1 = [init_weights_l1]
        weights_l2 = [init_weights_l2]
        weights_l3 = [init_weights_l3]
        biases_l1 = [init_biases_l1]
        biases_l2 = [init_biases_l2]
        biases_l3 = [init_biases_l3]
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        length_of_bar = 20
        epoch_bar_size = 0
        print(f"    Epoch (1/{training_epochs})")
        epoch_start_time = time.time()
        for evolving in range(number_of_iterations):
            cost_list = []
            for sample in range(len(weights_l1)):
                output = layer_foward(training_inputs, weights_l1[sample], biases_l1[sample])
                output = layer_foward(output, weights_l2[sample], biases_l2[sample])
                output = layer_foward(output, weights_l3[sample], biases_l3[sample])
                cost = sum(sum(abs(output - training_expectations) * abs(output - training_expectations)))
                cost_list.append(cost)
            best_index = cost_list.index(min(cost_list))
            if evolving % 100 == 0:
                bar_filled = "="
                bar_unfilled = "."
                if evolving - epoch_bar_size > epoch_size-1 :
                    epoch_bar_size += epoch_size
                    print(f"    [{bar_filled * length_of_bar}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
                    print(f"\n    Epoch ({epoch_bar_size//epoch_size+1}/{training_epochs})")
                    epoch_start_time = time.time()
                print(f"    [{bar_filled * ((evolving - epoch_bar_size) // (epoch_size // length_of_bar) + 1)}{bar_unfilled * (length_of_bar - ((evolving - epoch_bar_size) // (epoch_size // length_of_bar)) - 1)}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
            weights_l1 = [weights_l1[best_index]]
            weights_l2 = [weights_l2[best_index]]
            weights_l3 = [weights_l3[best_index]]
            biases_l1 = [biases_l1[best_index]]
            biases_l2 = [biases_l2[best_index]]
            biases_l3 = [biases_l3[best_index]]
            for iterations in range(10):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.001, 0.001, (16,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.001, 0.001, (16,16)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs,16)))
            for iterations in range(10):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.001, 0.001, (16)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.001, 0.001, (16)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs)))
            for iterations in range(9):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.0001, 0.0001, (16,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.0001, 0.0001, (16,16)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.0001, 0.0001, (number_of_outputs,16)))
            for iterations in range(9):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.0001, 0.0001, (16)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.0001, 0.0001, (16)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.0001, 0.0001, (number_of_outputs)))
        data = []
        data.append("wl1=["+str(list(weights_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl2=["+str(list(weights_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl3=["+str(list(weights_l3[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl1=["+str(list(biases_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl2=["+str(list(biases_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl3=["+str(list(biases_l3[0])).replace("array(", "").replace(")", "")+"]")
        textfile = open("nait_model.py", "w")
        for line in data:
            textfile.write(line+"\n")
        textfile.close()
        print(f"    [{bar_filled * length_of_bar}] 100% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ")
        print(f"    Data saved to 'nait_model.py'                                                                                \n    Final accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Final loss: {min(cost_list):.9f} Total time: {round(time.time() - start_time, 1)}s")
    def load(loading_inputs):
        from nait_model import wl1, wl2, wl3, bl1, bl2, bl3
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        output = layer_foward(loading_inputs, wl1[0], bl1[0])
        output = layer_foward(output, wl2[0], bl2[0])
        output = layer_foward(output, wl3[0], bl3[0])
        return output
class complex():
    def train(training_inputs, training_expectations, training_epochs):
        start_time = time.time()
        if isinstance(training_inputs, list) == False:
            raise ValueError(f"{training_inputs} should be type 'list'")
        if isinstance(training_expectations, list) == False:
            raise ValueError(f"{training_expectations} should be type 'list'")
        if isinstance(training_inputs[0], list) == False:
            raise ValueError(f"{training_inputs[0]} should be type 'list'")
        if isinstance(training_expectations[0], list) == False:
            raise ValueError(f"{training_expectations[0]} should be type 'list'")
        if len(training_inputs) != len(training_expectations):
            raise IndexError(f"{training_inputs} should be the same length as {training_expectations}")
        if isinstance(training_inputs[0][0], int) == False and isinstance(training_inputs[0][0], float) == False:
            raise ValueError(f"{training_inputs[0][0]} should be type 'integer' or 'float'")
        if isinstance(training_expectations[0][0], int) == False and isinstance(training_expectations[0][0], float) == False:
            raise ValueError(f"{training_expectations[0][0]} should be type 'integer' or 'float'")
        number_of_inputs = len(training_inputs[0])
        number_of_outputs = len(training_expectations[0])
        version = "1.1.0"
        epoch_size = 1000
        number_of_iterations = epoch_size * training_epochs
        os.system(f'title NAIT {version}')
        init_weights_l1 = [[1/number_of_inputs]*number_of_inputs]*64
        init_weights_l2 = [[1/64]*64]*64
        init_weights_l3 = [[1/64]*64]*number_of_outputs
        init_biases_l1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l3 = [0]*number_of_outputs
        weights_l1 = [init_weights_l1]
        weights_l2 = [init_weights_l2]
        weights_l3 = [init_weights_l3]
        biases_l1 = [init_biases_l1]
        biases_l2 = [init_biases_l2]
        biases_l3 = [init_biases_l3]
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        length_of_bar = 20
        epoch_bar_size = 0
        print(f"    Epoch (1/{training_epochs})")
        epoch_start_time = time.time()
        for evolving in range(number_of_iterations):
            cost_list = []
            for sample in range(len(weights_l1)):
                output = layer_foward(training_inputs, weights_l1[sample], biases_l1[sample])
                output = layer_foward(output, weights_l2[sample], biases_l2[sample])
                output = layer_foward(output, weights_l3[sample], biases_l3[sample])
                cost = sum(sum(abs(output - training_expectations) * abs(output - training_expectations)))
                cost_list.append(cost)
            best_index = cost_list.index(min(cost_list))
            if evolving % 100 == 0:
                bar_filled = "="
                bar_unfilled = "."
                if evolving - epoch_bar_size > epoch_size-1 :
                    epoch_bar_size += epoch_size
                    print(f"    [{bar_filled * length_of_bar}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
                    print(f"\n    Epoch ({epoch_bar_size//epoch_size+1}/{training_epochs})")
                print(f"    [{bar_filled * ((evolving - epoch_bar_size) // (epoch_size // length_of_bar) + 1)}{bar_unfilled * (length_of_bar - ((evolving - epoch_bar_size) // (epoch_size // length_of_bar)) - 1)}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
            weights_l1 = [weights_l1[best_index]]
            weights_l2 = [weights_l2[best_index]]
            weights_l3 = [weights_l3[best_index]]
            biases_l1 = [biases_l1[best_index]]
            biases_l2 = [biases_l2[best_index]]
            biases_l3 = [biases_l3[best_index]]
            for iterations in range(10):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.001, 0.001, (64,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.001, 0.001, (64,64)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs,64)))
            for iterations in range(10):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.001, 0.001, (64)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.001, 0.001, (64)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs)))
            for iterations in range(9):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.0001, 0.0001, (64,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.0001, 0.0001, (64,64)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs,64)))
            for iterations in range(9):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.0001, 0.0001, (64)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.0001, 0.0001, (64)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.0001, 0.0001, (number_of_outputs)))
        data = []
        data.append("wl1=["+str(list(weights_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl2=["+str(list(weights_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl3=["+str(list(weights_l3[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl1=["+str(list(biases_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl2=["+str(list(biases_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl3=["+str(list(biases_l3[0])).replace("array(", "").replace(")", "")+"]")
        textfile = open("nait_model.py", "w")
        for line in data:
            textfile.write(line+"\n")
        textfile.close()
        print(f"    [{bar_filled * length_of_bar}] 100% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ")
        print(f"    Data saved to 'nait_model.py'                                                                                \n    Final accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Final loss: {min(cost_list):.9f} Total time: {round(time.time() - start_time, 1)}s")
    def load(loading_inputs):
        from nait_model import wl1, wl2, wl3, bl1, bl2, bl3
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        output = layer_foward(loading_inputs, wl1[0], bl1[0])
        output = layer_foward(output, wl2[0], bl2[0])
        output = layer_foward(output, wl3[0], bl3[0])
        return output
class simple():
    def train(training_inputs, training_expectations, training_epochs):
        start_time = time.time()
        if isinstance(training_inputs, list) == False:
            raise ValueError(f"{training_inputs} should be type 'list'")
        if isinstance(training_expectations, list) == False:
            raise ValueError(f"{training_expectations} should be type 'list'")
        if isinstance(training_inputs[0], list) == False:
            raise ValueError(f"{training_inputs[0]} should be type 'list'")
        if isinstance(training_expectations[0], list) == False:
            raise ValueError(f"{training_expectations[0]} should be type 'list'")
        if len(training_inputs) != len(training_expectations):
            raise IndexError(f"{training_inputs} should be the same length as {training_expectations}")
        if isinstance(training_inputs[0][0], int) == False and isinstance(training_inputs[0][0], float) == False:
            raise ValueError(f"{training_inputs[0][0]} should be type 'integer' or 'float'")
        if isinstance(training_expectations[0][0], int) == False and isinstance(training_expectations[0][0], float) == False:
            raise ValueError(f"{training_expectations[0][0]} should be type 'integer' or 'float'")
        number_of_inputs = len(training_inputs[0])
        number_of_outputs = len(training_expectations[0])
        version = "1.1.0"
        epoch_size = 1000
        number_of_iterations = epoch_size * training_epochs
        os.system(f'title NAIT {version}')
        init_weights_l1 = [[1/number_of_inputs]*number_of_inputs]*8
        init_weights_l2 = [[1/8]*8]*8
        init_weights_l3 = [[1/8]*8]*number_of_outputs
        init_biases_l1 = [0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l2 = [0, 0, 0, 0, 0, 0, 0, 0]
        init_biases_l3 = [0]*number_of_outputs
        weights_l1 = [init_weights_l1]
        weights_l2 = [init_weights_l2]
        weights_l3 = [init_weights_l3]
        biases_l1 = [init_biases_l1]
        biases_l2 = [init_biases_l2]
        biases_l3 = [init_biases_l3]
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        length_of_bar = 20
        epoch_bar_size = 0
        print(f"    Epoch (1/{training_epochs})")
        epoch_start_time = time.time()
        for evolving in range(number_of_iterations):
            cost_list = []
            for sample in range(len(weights_l1)):
                output = layer_foward(training_inputs, weights_l1[sample], biases_l1[sample])
                output = layer_foward(output, weights_l2[sample], biases_l2[sample])
                output = layer_foward(output, weights_l3[sample], biases_l3[sample])
                cost = sum(sum(abs(output - training_expectations) * abs(output - training_expectations)))
                cost_list.append(cost)
            best_index = cost_list.index(min(cost_list))
            if evolving % 100 == 0:
                bar_filled = "="
                bar_unfilled = "."
                if evolving - epoch_bar_size > epoch_size-1 :
                    epoch_bar_size += epoch_size
                    print(f"    [{bar_filled * length_of_bar}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
                    print(f"\n    Epoch ({epoch_bar_size//epoch_size+1}/{training_epochs})")
                print(f"    [{bar_filled * ((evolving - epoch_bar_size) // (epoch_size // length_of_bar) + 1)}{bar_unfilled * (length_of_bar - ((evolving - epoch_bar_size) // (epoch_size // length_of_bar)) - 1)}] {evolving // (number_of_iterations // 100)}% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ", end = "\r")
            weights_l1 = [weights_l1[best_index]]
            weights_l2 = [weights_l2[best_index]]
            weights_l3 = [weights_l3[best_index]]
            biases_l1 = [biases_l1[best_index]]
            biases_l2 = [biases_l2[best_index]]
            biases_l3 = [biases_l3[best_index]]
            for iterations in range(10):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.001, 0.001, (8,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.001, 0.001, (8,8)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs,8)))
            for iterations in range(10):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.001, 0.001, (8)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.001, 0.001, (8)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.001, 0.001, (number_of_outputs)))
            for iterations in range(9):
                weights_l1.append(weights_l1[0]+np.random.uniform(-0.0001, 0.0001, (8,number_of_inputs)))
                weights_l2.append(weights_l2[0]+np.random.uniform(-0.0001, 0.0001, (8,8)))
                weights_l3.append(weights_l3[0]+np.random.uniform(-0.0001, 0.0001, (number_of_outputs,8)))
            for iterations in range(9):
                biases_l1.append(biases_l1[0]+np.random.uniform(-0.0001, 0.0001, (8)))
                biases_l2.append(biases_l2[0]+np.random.uniform(-0.0001, 0.0001, (8)))
                biases_l3.append(biases_l3[0]+np.random.uniform(-0.0001, 0.0001, (number_of_outputs)))
        data = []
        data.append("wl1=["+str(list(weights_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl2=["+str(list(weights_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("wl3=["+str(list(weights_l3[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl1=["+str(list(biases_l1[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl2=["+str(list(biases_l2[0])).replace("array(", "").replace(")", "")+"]")
        data.append("bl3=["+str(list(biases_l3[0])).replace("array(", "").replace(")", "")+"]")
        textfile = open("nait_model.py", "w")
        for line in data:
            textfile.write(line+"\n")
        textfile.close()
        print(f"    [{bar_filled * length_of_bar}] 100% Accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Loss: {min(cost_list):.9f} {round(time.time() - epoch_start_time, 1)}s                    ")
        print(f"    Data saved to 'nait_model.py'                                                                                \n    Final accuracy: {1 - ((sigmoid(min(cost_list)*10)-0.5)*2):.9f} Final loss: {min(cost_list):.9f} Total time: {round(time.time() - start_time, 1)}s")
    def load(loading_inputs):
        from nait_model import wl1, wl2, wl3, bl1, bl2, bl3
        def layer_foward(function_input, function_weights, function_biases):
            return np.dot(function_input, np.array(function_weights).T) + function_biases
        output = layer_foward(loading_inputs, wl1[0], bl1[0])
        output = layer_foward(output, wl2[0], bl2[0])
        output = layer_foward(output, wl3[0], bl3[0])
        return output