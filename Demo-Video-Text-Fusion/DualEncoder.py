class DualEncoder(keras.Model):
    def __init__(self, text_encoder, image_encoder, temperature=1.0, **kwargs):
        super().__init__(**kwargs)
        self.text_encoder = text_encoder
        self.image_encoder = image_encoder
        self.temperature = temperature
        self.loss_tracker = keras.metrics.Mean(name="loss")

    @property
    def metrics(self):
        return [self.loss_tracker]

    def call(self, features, training=False):
        # Place each encoder on a separate GPU (if available).
        # TF will fallback on available devices if there are fewer than 2 GPUs.
        with tf.device("/gpu:0"):
            # Get the embeddings for the captions.
            caption_embeddings = text_encoder(features["caption"], training=training)
        with tf.device("/gpu:1"):
            # Get the embeddings for the images.
            image_embeddings = vision_encoder(features["image"], training=training)
        return caption_embeddings, image_embeddings

   def compute_loss(self, caption_embeddings, image_embeddings):
        # Calculate cosine similarity.
        similarity = tf.keras.losses.CosineSimilarity(axis=-1)(caption_embeddings, image_embeddings)

        # Use the temperature-scaled similarity as logits for softmax.
        logits = similarity / self.temperature

        # Compute softmax probabilities.
        probs = tf.nn.softmax(logits, axis=-1)

        # Create a mask for negative pairs.
        negative_mask = 1.0 - tf.eye(tf.shape(logits)[0])

        # Calculate the denominator for NT-Xent.
        denominator = tf.reduce_sum(tf.exp(logits * self.temperature) * negative_mask, axis=-1, keepdims=True)

        # Calculate NT-Xent loss.
        loss = -tf.reduce_mean(tf.math.log(tf.clip_by_value(probs, 1e-10, 1.0) / denominator))

        return loss


    def train_step(self, features):
        with tf.GradientTape() as tape:
            # Forward pass
            caption_embeddings, image_embeddings = self(features, training=True)
            loss = self.compute_loss(caption_embeddings, image_embeddings)
        # Backward pass
        gradients = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        # Monitor loss
        self.loss_tracker.update_state(loss)
        return {"loss": self.loss_tracker.result()}

    def test_step(self, features):
        caption_embeddings, image_embeddings = self(features, training=False)
        loss = self.compute_loss(caption_embeddings, image_embeddings)
        self.loss_tracker.update_state(loss)
        return {"loss": self.loss_tracker.result()}
