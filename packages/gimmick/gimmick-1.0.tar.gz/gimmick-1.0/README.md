# gimmick

## Introduction
Whats Gimmick ? Its a library which allows us to generate images out of nothing, basically you tell gimmick what kind of images you would like to generate and what model to use and it does the rest.
Its easy to use as primary focus is on user friendlyness without exposing to much details, but you can be specific if you wanna be.

What do we do internally ? we trained neuralnets, we add different type of networks making sure that interface always remain same, just plugin different algo and see how it perform.

## Installtion
<pre>pip install gimmick</pre>
just like that, its python everything should be easy

## Dependency
Gimmick autmatically install all the dependency for you, but occationaly you run into one of those bugs, so in a nutshell we use tensorflow, sklearn.
i know torch is much faster, we will get their

## Examples
we have already provided samples with the github repo, you can browse it, read it and run it.

Lets demonstrate

### usecase 1 - I just wanna run as simple as i can.
<pre>
import gimmick
model = gimmick.learn(images, algo='autoencoder_dense')  # Just make sure that images is a numpy array which contains N number 3D or 2D images
images_gen = model.generate(16)  # I need 16 images
</pre>

### usecase 2 - I wanna control how my model is trained
<pre>
import gimmick
model = gimmick.learn(images, algo='autoencoder_dense', epochs=500, batch_size=8,
                      optimizer='adam', learning_rate=0.01, loss_function='mae')
images_gen = model.generate(16, batch_size=8)
</pre>

### usecase 3 - I wanna know everything

Go through the detailed documentation.


