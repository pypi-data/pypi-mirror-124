import os
from typing import Union, Optional, Callable, Dict, Tuple
from functools import partial

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Optimizer

from quple.models import AbstractModel

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

try:
    from IPython.display import clear_output
except ImportError:
    clear_output = None

class QGAN(AbstractModel):
    """Quantum Generative Adversarial Network (QGAN)
    """    
    def __init__(self, generator:Model, 
                 discriminator:Model,
                 latent_dim:Optional[Union[int, Tuple]]=None,
                 n_disc:int=1,
                 n_gen:int=1,
                 epochs:int=100, 
                 batch_size:int=32,
                 optimizer:Optional[Union[str, Dict]]=None,
                 optimizer_kwargs:Optional[Dict]=None,
                 name:str='QGAN',
                 random_state:Optional[int]=None,
                 checkpoint_dir:Optional[str]=None,
                 checkpoint_interval:int=10,
                 checkpoint_max_to_keep:Optional[int]=None):
        """ Creates a QGAN model equipped with a generator and a discriminator neural networks.
            The modified Jensen-Shanon divergence is used as the loss function.
        Args:
            generator: tensorflow.keras.Model
                A keras model representing the generator neural network. It can contain
                both classical and quantum layers.
            discriminator: cirq.Circuit or quple.QuantumCircuit instace
                A keras model representing the discriminator neural network. It can contain
                both classical and quantum layers.
            latent_dim: (Optional) int or tuple of int
                Dimensions of the latent space. It specifies the shape of the input noise
                (drawn from a normal distribution) passed to the generator neural network.
            n_disc: (Optional) int, default=1
                Number of discriminator iterations per generator iteration in each epoch.
            n_disc: (Optional) int, default=1
                Number of generatator iterations per discriminator iteration in each epoch.                
            epochs: int, default=100
                Number of epochs for the training.
            batch_size: int, default=10
                Number of training examples used in one iteration. Note that the true batch
                size is batch_size * n_disc so that training samples of size batch_size is
                passed to the discriminator in each discriminator step.
            name: (Optional) string
                Name given to the model.
            random_state: (Optional) int
                The random state used at the beginning of a training
                for reproducible result.
            checkpoint_dir: Optional[string]
                The path to a directory in which to write checkpoints. If None,
                no checkpoint will be saved.
            checkpoint_interval: int, default=10
                Number of epochs between each checkpoint.
            checkpoint_max_to_keep: (Optional) int
                Number of checkpoints to keep. If None, all checkpoints are kept.
        """
        self.set_random_state(random_state)
        
        self.start_epoch = 0
        self.n_disc = n_disc
        self.n_gen  = n_gen
        self.epochs = epochs
        self.batch_size = batch_size

        if not isinstance(generator, Model):
            raise ValueError("generator must be a tf.keras.Model instance")
        self.G = generator
        if not isinstance(discriminator, Model):
            raise ValueError("discriminator must be a tf.keras.Model instance")            
        self.D = discriminator
        
        if latent_dim is None:
            try:
                self.latent_dim = self.G.input_shape[1:]
            except:
                raise RuntimeError("cannot infer input shape from generator")
        else:
            self.latent_dim = tuple(latent_dim)
        self.z_batch_shape = (self.batch_size,) + self.latent_dim            

        self.G_optimizer, self.D_optimizer = self._get_optimizers(optimizer, optimizer_kwargs)
        
        self.loss_function = self._get_loss_function()
        
        self.visualization_interval = None
        self.image_shape = None
        self.n_image_to_show = 0
        self.cmap = 'viridis'
        self.colorbar = True
        self.detailed_loss = True
        self.vrange = None
        self.batch_mode = False
        
        print('Summary of Generator')
        self.G.summary()
        
        print('Summary of Discriminator')
        self.D.summary()
        
        self.reset()
        
        super().__init__(name=name, random_state=random_state,
                         checkpoint_dir=checkpoint_dir,
                         checkpoint_interval=checkpoint_interval,
                         checkpoint_max_to_keep=checkpoint_max_to_keep)

    def _create_checkpoint(self):
        checkpoint = tf.train.Checkpoint(step=tf.Variable(0),
                                         generator_optimizer=self.G_optimizer,
                                         discriminator_optimizer=self.D_optimizer,
                                         generator=self.G,
                                         discriminator=self.D,
                                         g_loss_arr=tf.Variable(tf.zeros(1000)),
                                         d_loss_arr=tf.Variable(tf.zeros(1000)),
                                         d_loss_real_arr=tf.Variable(tf.zeros(1000)),
                                         d_loss_fake_arr=tf.Variable(tf.zeros(1000)),
                                         epoch_arr=tf.Variable(tf.zeros(1000)))
        return checkpoint
        
        
    def _get_loss_function(self):
        return tf.keras.losses.BinaryCrossentropy(from_logits=True)
        
    @staticmethod
    def _get_optimizers(optimizer:Optional[Union[str, Dict]]=None,
                        optimizer_kwargs:Optional[Dict]=None):
        if isinstance(optimizer, str):
            optimizer = {"generator": optimizer, "discriminator": optimizer}
        elif isinstance(optimizer, dict):
            if ("generator" not in optimizer) or ("discriminator" not in optimizer):
                raise ValueError("optimizer passed as dictionary must contain both  "
                                 "`generator` and `discriminator` keys")
        else:
            raise ValueError("could not interpret optimizer: {}".format(optimizer))
        if optimizer_kwargs is None:
            optimizer_kwargs = {"generator": {}, "discriminator": {}}
        elif isinstance(optimizer_kwargs, dict):
            if ("generator" not in optimizer_kwargs) and ("discriminator" not in optimizer_kwargs):
                optimizer_kwargs = {"generator": optimizer_kwargs, "discriminator": optimizer_kwargs}
            elif ("generator" not in optimizer_kwargs) or ("discriminator" not in optimizer_kwargs):
                raise ValueError("optimizer_kwargs passed as dictionary must contain both  "
                                 "`generator` and `discriminator` keys")
        resolved = {}
        for key in ["generator", "discriminator"]:
            identifier = optimizer[key]
            config = optimizer_kwargs[key]
            if isinstance(identifier, Optimizer):
                resolved[key] = identifier
            elif isinstance(identifier, dict):
                identifier.update(kwargs)
                resolved[key] = tf.keras.optimizers.get(identifier)
            elif isinstance(identifier, str):
                identifier = {"class_name": str(identifier), "config": config}
                resolved[key] = tf.keras.optimizers.get(identifier)
            else:
                raise ValueError("could not interpret identifier: {}".format(identifier))
        generator_optimizer = resolved["generator"]
        discriminator_optimizer = resolved["discriminator"]
        return generator_optimizer, discriminator_optimizer
                        
    
    @tf.function
    def D_loss(self, real_output, fake_output):
        """Compute discriminator loss."""
        loss_real = self.loss_function(tf.ones_like(real_output), real_output)
        loss_fake = self.loss_function(tf.zeros_like(fake_output), fake_output)
        loss      = loss_real + loss_fake
        return loss, loss_real, loss_fake
    
    @tf.function
    def G_loss(self, fake_output):
        """Compute generator loss."""
        return self.loss_function(tf.ones_like(fake_output), fake_output)
    
    @tf.function
    def train_step_1v1(self, x_real):
        """Training step for one epoch with 1 generator step and 1 discriminator step
        """
        z = tf.random.normal(self.z_batch_shape)
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            x_fake_ = self.G(z, training=True)
            x_fake = tf.reshape(x_fake_, tf.shape(x_real))
            real_output = self.D(x_real, training=True)
            fake_output = self.D(x_fake, training=True)
            g_loss = self.G_loss(fake_output)
            d_loss, d_loss_real, d_loss_fake = self.D_loss(real_output, fake_output)
        grad_gen = gen_tape.gradient(g_loss, self.G.trainable_variables)
        grad_disc = disc_tape.gradient(d_loss, self.D.trainable_variables)
        self.G_optimizer.apply_gradients(zip(grad_gen, self.G.trainable_variables))
        self.D_optimizer.apply_gradients(zip(grad_disc, self.D.trainable_variables))  
        return g_loss, d_loss, d_loss_real, d_loss_fake
    
    @tf.function 
    def G_step(self):
        """Perform one training step for generator"""
        # using Gaussian noise with mean 0 and width 1 as generator input
        z = tf.random.normal(self.z_batch_shape)
        with tf.GradientTape() as t:
            x_fake = self.G(z, training=True)
            fake_output = self.D(x_fake, training=True)
            g_loss = self.G_loss(fake_output)
        grad = t.gradient(g_loss, self.G.trainable_variables)
        self.G_optimizer.apply_gradients(zip(grad, self.G.trainable_variables))
        return g_loss
    
    @tf.function
    def D_step(self, x_real):
        """Perform one training step for discriminator
        
            Arguments:
                x_real: Numpy array, tf.Tensor / any inputs accepted by tensorflow
                    Input from the real data.
        """
        # using Gaussian noise with mean 0 and width 1 as generator input
        z = tf.random.normal(self.z_batch_shape)
        with tf.GradientTape() as t:
            x_fake_ = self.G(z, training=True)
            x_fake = tf.reshape(x_fake_, tf.shape(x_real))
            real_output = self.D(x_real, training=True)
            fake_output = self.D(x_fake, training=True)
            d_loss, d_loss_real, d_loss_fake = self.D_loss(real_output, fake_output)
        grad = t.gradient(d_loss, self.D.trainable_variables)
        self.D_optimizer.apply_gradients(zip(grad, self.D.trainable_variables))
        return d_loss, d_loss_real, d_loss_fake
    
    @tf.function
    def train_step_nv1(self, x_real):
        """Training step for one epoch with 1 generator step and n_disc discriminator step"""
        for i in range(self.n_disc):
            x_real_batch = tf.gather(x_real, i)
            d_loss, d_loss_real, d_loss_fake = self.D_step(x_real_batch)
        g_loss = self.G_step()
        return g_loss, d_loss, d_loss_real,d_loss_fake

    @tf.function
    def train_step_1vn(self, x_real):
        """Training step for one epoch with n_gen generator step and 1 discriminator step"""
        for i in range(self.n_gen):
            g_loss = self.G_step()
        d_loss, d_loss_real, d_loss_fake = self.D_step(x_real)
        return g_loss, d_loss, d_loss_real, d_loss_fake
    
    def generate_samples(self, batch_size:int, shape:Optional[Tuple[int]]=None):
        """Generates sample using random inputs
        
            Arguments:
                batch_size: int
                    Number of samples to generate.
                shape: (Optional) tuple of int
                    Reshape the output to the given shape.
        """
        z_batch_shape = (batch_size,) + self.latent_dim
        z = tf.random.normal(z_batch_shape)
        samples = self.G(z, training=False)  
        if shape is not None:
            shape = (batch_size,) + shape
            samples = tf.reshape(samples, shape)
        return samples
    
    def predict(self, x):
        """Get predicted output from discriminator
        
            Arguments:
                x: Numpy array, tf.Tensor / any inputs accepted by tensorflow
                    Input data.
            Returns:
                tf.Tensor representing the predicted output from discriminator
        """
        return self.D(x, training=False)
    
    def reset(self):
        self.g_loss_arr      = []
        self.d_loss_arr      = []
        self.d_loss_real_arr = []
        self.d_loss_fake_arr = []
        self.epoch_arr       = []

    def train(self, x):
        """Train a GAN model
        
            Arguments:
                x: Numpy array, tf.Tensor / any inputs accepted by tensorflow
                    Input data.        
        """
        self._train_preprocess()
        dataset = self.prepare_dataset(x, batch_size=self.batch_size * self.n_disc,
                                       seed=self.random_state)
        g_metric      = tf.keras.metrics.Mean()
        d_metric      = tf.keras.metrics.Mean()
        d_metric_real = tf.keras.metrics.Mean() 
        d_metric_fake = tf.keras.metrics.Mean()
        
        input_shape = x.shape[1:]
        if (self.n_disc == 1) and (self.n_gen == 1):
            train_step = self.train_step_1v1
            input_batch_shape = (self.batch_size,) + input_shape
        elif (self.n_disc > 1) and (self.n_gen == 1):
            train_step = self.train_step_nv1
            input_batch_shape = (self.n_disc, self.batch_size) + input_shape
        elif (self.n_disc == 1) and (self.n_gen > 1):
            train_step = self.train_step_1vn
            input_batch_shape = (self.batch_size,) + input_shape
        else:
            raise RuntimeError("n_disc > 1 and n_gen > 1 are not supported")
            
        for epoch in range(self.epochs):
            for step, x_batch_train_ in enumerate(dataset):
                # for restoring dataset at checkpoint
                if self.start_epoch > epoch:
                    continue
                x_batch_train = tf.reshape(x_batch_train_, input_batch_shape)
                gen_loss, disc_loss, disc_loss_real, disc_loss_fake = train_step(x_batch_train)
                g_metric(gen_loss)
                d_metric(disc_loss)
                d_metric_real(disc_loss_real)
                d_metric_fake(disc_loss_fake)
            if self.start_epoch > epoch:
                continue
            g_loss = g_metric.result().numpy()
            d_loss = d_metric.result().numpy()
            d_loss_real = d_metric_real.result().numpy()
            d_loss_fake = d_metric_fake.result().numpy()
            self.g_loss_arr.append(g_loss)
            self.d_loss_arr.append(d_loss)
            self.d_loss_real_arr.append(d_loss_real)
            self.d_loss_fake_arr.append(d_loss_fake)
            self.epoch_arr.append(epoch)
            
            self._train_post_epoch(epoch, g_loss, d_loss, d_loss_real, d_loss_fake)
            g_metric.reset_states()
            d_metric.reset_states()
            d_metric_real.reset_states()
            d_metric_fake.reset_states()
        
        self._train_postprocess()
        
    def _train_post_epoch(self, epoch:int, g_loss, d_loss, d_loss_real, d_loss_fake, *args, **kwargs):
        if (self.checkpoint is not None) and (self.checkpoint_manager is not None):
            self.checkpoint.g_loss_arr[epoch].assign(g_loss)
            self.checkpoint.d_loss_arr[epoch].assign(d_loss)
            self.checkpoint.d_loss_real_arr[epoch].assign(d_loss_real)
            self.checkpoint.d_loss_fake_arr[epoch].assign(d_loss_fake)
        super()._train_post_epoch(epoch, *args, **kwargs)
        if self.visualization_interval and ((epoch + 1) % self.visualization_interval == 0):
            self.display_loss_and_image(self.g_loss_arr, self.d_loss_arr, self.epoch_arr,
                                        self.d_loss_real_arr, self.d_loss_fake_arr)
            
    def restore_checkpoint(self, checkpoint:tf.train.Checkpoint=None):
        super().restore_checkpoint(checkpoint)
        self.g_loss_arr = list(self.checkpoint.g_loss_arr[:self.checkpoint.step].numpy())
        self.d_loss_arr = list(self.checkpoint.d_loss_arr[:self.checkpoint.step].numpy())
        self.d_loss_real_arr = list(self.checkpoint.d_loss_real_arr[:self.checkpoint.step].numpy())
        self.d_loss_fake_arr = list(self.checkpoint.d_loss_fake_arr[:self.checkpoint.step].numpy())
        self.epoch_arr = list(range(self.checkpoint.step.numpy()))
        
    def enable_visualization(self, image_shape:Tuple[int], n_image:int=16, 
                             interval:int=1, detailed_loss:bool=True,
                             cmap:str='viridis', colorbar:bool=True,
                             vrange:Optional[Tuple]=None,
                             batch_mode:bool=False):
        """Enable visualization of loss curve and generated images
        
            Arguments:
                image_shape: tuple of int
                    Dimensions of the image of the form (rows, cols).
                n_image: int, default=16
                    Number of images to show.
                interval: int, default=1
                    Number of epochs between each update.
        """
        self.image_shape = image_shape
        self.visualization_interval = interval
        self.n_image_to_show = n_image
        self.cmap = cmap
        self.colorbar = colorbar
        self.detailed_loss = detailed_loss
        self.vrange = vrange
        self.batch_mode = batch_mode
    
    def disable_visualization(self):
        self.visualization_interval = None
    
    def display_loss_and_image(self, g_loss, d_loss, epochs, 
                               d_loss_real=None,
                               d_loss_fake=None):
        if clear_output is not None:
            clear_output(wait=True)
        fig = plt.figure(figsize=(16,9))
        size = max(self.n_image_to_show, 1)
        rows = ( size // 4 ) + 1
        gs = gridspec.GridSpec(ncols=8, nrows=rows, figure=fig)
        epoch = epochs[-1]
        # plot loss curve
        ax_loss = plt.subplot(gs[:,:4])
        ax_loss.set_xlim(0, 1.1*epoch)
        ax_loss.plot(epochs, g_loss, label="Generator")
        ax_loss.plot(epochs, d_loss, label="Discriminator")
        if (self.detailed_loss) and (d_loss_real is not None) and (d_loss_fake is not None):
            ax_loss.plot(epochs, d_loss_real, label="Disc real")
            ax_loss.plot(epochs, d_loss_fake, label="Disc fake")
        ax_loss.set_xlabel('Epoch', fontsize=20)
        ax_loss.set_ylabel('Loss', fontsize=20)
        ax_loss.grid(True)
        ax_loss.legend(fontsize=15)
        if self.vrange is None:
            vmin = None
            vmax = None
        else:
            vmin = self.vrange[0]
            vmax = self.vrange[1]
        if (self.image_shape is not None):
            images = self.generate_samples(self.n_image_to_show, self.image_shape)
            prediction = self.predict(images)
            for i in range(images.shape[0]):
                ax = plt.subplot(gs[i//4, 4 + i%4])
                ax.set_title("score: {:.4f}".format(prediction[i][0]))
                im = plt.imshow(images[i], vmin=vmin, vmax=vmax, cmap=self.cmap)
            if self.colorbar:
                plt.colorbar(im)
            plt.tight_layout()
        if self.checkpoint_dir:
            if not os.path.exists(self.checkpoint_dir):
                os.makedirs(self.checkpoint_dir, exist_ok=True)
            image_path = os.path.join(self.checkpoint_dir, 'image_at_epoch_{:04d}.png'.format(epoch))
            plt.savefig(image_path)
        if not self.batch_mode:
            plt.show()