import tensorflow as tf

def createModel(train_x):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=train_x.shape[1:]),
        #input shape is IMG_SIZExIMG_SIZEx3bytes coloured (HSV))
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(), #flattens the dataset for our input layer
        tf.keras.layers.Dense(512,activation=tf.nn.relu),
        tf.keras.layers.Dense(6,activation='softmax') #sigmoid for final layer
    ])
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    return model