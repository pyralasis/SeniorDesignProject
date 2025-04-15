# Models

## What is a Model
A Model is a fully realized version of your neural network architecture, capturing all the parameters needed for training and inference. Once you convert an architecture into a model, you can train it on your chosen data using various optimizers, loss functions, and hyperparameters.

## Usage
### Creating a Model
From the Architecture page you can select an existing architecture and click `Convert To Model`
![image](https://github.com/user-attachments/assets/75fc5376-6c7b-4213-931c-1a01bd9a703e)
From there you will be given the option to name it and then click `Convert` to creat an instance of a model using your architecture blueprint.
![image](https://github.com/user-attachments/assets/57ed829e-1f46-491f-a3a1-baaf828e7447)

### Training Setup
Once you have created your model from an architecture you will find it on the Models page under your list of models.
![image](https://github.com/user-attachments/assets/885b542e-9901-40ef-bdcb-f6372b316658)
To start training setup, simply click one of the models and a set of parameters will appear at the bottom of your screen.
![image](https://github.com/user-attachments/assets/09845664-bbfd-49ce-8f82-7023247b5187)
Begin filling out the parameters to optimize the training for the model you have created.

Select the pipeline you created for this model from the `Data Source` drop down, and select one of the two available optimizers.

To edit the properties of your optimizer, click the pencil icon to the right of the dropdown - this will open a flyout from which you can provide values like Learning Rate, Beta 1 & 2, Epsilon, and Weight Decay

![image](https://github.com/user-attachments/assets/1ed59eb6-8f55-4dec-9043-9de1fd8178e7)

![image](https://github.com/user-attachments/assets/18153a95-cf8e-4c26-ad4d-ad4130d6d7f8)

You also have access to `Advanced Settings` by clicking the gear icon next to the Batch Size parameter, where you can set which proccessing unit you would like to train on, as well and number of workers and Prefetch Factor.

![image](https://github.com/user-attachments/assets/508aad88-e2d2-491d-8d7f-fa9e2a34f07e)

### Train
Once you have filled out every required parameter you can procceed with clicking the `Train` button

![image](https://github.com/user-attachments/assets/80c6400c-c01b-45cb-b63d-2061dcdc8bef)

This will add the model to a queue of models to train. If there are no models training it will be added to the In Progress list. You can see the status of your training on the Training page

![image](https://github.com/user-attachments/assets/a213d41e-f6ce-4665-9cdf-5b91817f7174)

Here you can also see the progress your model has made via the Current Epoch Ratio in the table.

Once the training is complete, if it doesn't fail, it will appear in the Complete table. From here you can access the PyTorch trained model from the models file within the app, or you can retrain it by clicking on the table row and clicking retrain.
![image](https://github.com/user-attachments/assets/9b551251-b3f5-44ec-9dc9-ccb3dfedd969)

