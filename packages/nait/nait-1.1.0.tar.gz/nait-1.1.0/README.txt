NAIT (Neural Artificial Intelligence Tool)

NAIT is a module for easily training and using neural networks.
Its developed so that people with little to no knowledge of neural networks can use it.


Usage
--------------------

    To train a network:

        Training model setup:

            To train the network you will need a training model, a training model consist of 2 lists.
            The first list contains all the input sets.
            every input set is a list of numbers either integer or floats.
            example of inputs: (training_inputs = [ [1, 1, 1, 1], [1, 1, 1, 1] ])
            The second list contains outputs that the ai should give for a sertain inputs.
            the index that the output sets have corresponds to the same index in the inputs list.
            the outputs must also be integers or floats.
            what the ai gets from this is that if you get these inputs you should output these outputs.
            example of inputs: (training_expectations = [ [2, 2, 2], [2, 2, 2] ])

        Actual training:

            Before you train your network with your training model you will first need to choose the complexity of your network.
            There is three levels of complexity: simple, standard and complex
            The more complex your network is, the longer it takes to train and the worse it might be at more basic tasks.
            You also need to decide for how long you want to train it for.
            You define how long it trains for in epochs which is 1000 generations each.
            Now to start the training you use the function: nait.<complexity>.train(<training inputs>, <training expectations>, <number of epochs>)
            You want to get the minimal loss and the maximum accuracy so if you are getting a high loss and low accuracy try some different settings.
            When the network is done training, it saves itself to 'nait_model.py', if there already is a 'nait_model.py' file, it overwrites it.

    To use a network:

        Setup:

            To use a network you first need a 'nait_model.py' file in the same directory.
            You now use the function nait.<complexity>.load(<inputs>)

        Inputs:
            
            You can input a pre-trained network a list of floats but the number of values must be the same as how the network was trained. (example: [1.0, 1.0, 1.0, 1.0])
            You can also give it multiple input lists at the same time. (example: [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]])
            It will then return an output of as many values as it was trained on. (example: [[10.0, 10.0], [20.0, 20.0]])


Example files
--------------------

Training example file: 
    import nait

    # training inputs to train the network on
    training_inputs = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]

    # training expectations to tell the network what outputs it should give for the inputs its given
    training_expectations = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]

    # training the network with the training models and defining how long you want to train it for
    nait.standard.train(training_inputs, training_expectations, 10)

Using example file: 
    import nait

    # a input set that you give the network
    inputs1 = [1, 1, 1, 1]

    # a list of inputs set to give the network
    inputs2 = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]

    # using the inputs and printing outputs
    print(nait.standard.load(inputs1))
    print(nait.standard.load(inputs2))