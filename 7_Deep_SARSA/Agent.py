import tensorflow as tf
import numpy as np
import random



flags = tf.app.flags

flags.n_input = 15
flags.n_hidden1 = 30
flags.n_hidden2 = 30
flags.n_output = 4

flags.learning_rate = 0.001
flags.discount_factor = 0.99
flags.epsilon_decay = 0.9999
flags.epsilon_min = 0.05

class Agent():
    def __init__(self, env):
        self.epsilon = 1.0
        self.possible_actions = env.possible_actions

        self.sess = tf.Session()

        self.x = tf.placeholder(dtype="float", shape=[None, flags.n_input])
        self.target = tf.placeholder(dtype="float", shape=[None, flags.n_output])

        self.pred = self.inference()
        self.loss, self.train = self.loss_and_train(self.pred)

        self.sess.run(tf.global_variables_initializer())

    def inference(self):

        weights = {
            'h1': tf.Variable(tf.random_normal([flags.n_input, flags.n_hidden1])),
            'h2': tf.Variable(tf.random_normal([flags.n_hidden1, flags.n_hidden2])),
            'o': tf.Variable(tf.random_normal([flags.n_hidden2, flags.n_output]))
        }
        biases = {
            'h1': tf.Variable(tf.random_normal([flags.n_hidden1])),
            'h2': tf.Variable(tf.random_normal([flags.n_hidden2])),
            'o': tf.Variable(tf.random_normal([flags.n_output]))
        }

        h_layer1 = tf.add(tf.matmul(self.x, weights['h1']), biases['h1'])
        h_layer1 = tf.nn.relu(h_layer1)

        h_layer2 = tf.add(tf.matmul(h_layer1, weights['h2']), biases['h2'])
        h_layer2 = tf.nn.relu(h_layer2)

        output = tf.matmul(h_layer2, weights['o']) + biases['o']

        return output

    def loss_and_train(self, pred):
        loss = tf.reduce_sum(tf.square(self.target - pred))
        train = tf.train.AdamOptimizer(flags.learning_rate).minimize(loss)

        return loss, train

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice(self.possible_actions)
        else:
            q_value = self.sess.run(self.pred, feed_dict={self.x: state})
            max_q_index = np.argmax(q_value, axis=1)[0]
            return self.possible_actions[max_q_index]

    def train_model(self, state, action, reward, next_state, next_action, done):
        if flags.epsilon_min < self.epsilon:
            self.epsilon *= flags.epsilon_decay

        target = self.sess.run(self.pred, feed_dict={self.x:state})
        next_q = self.sess.run(self.pred, feed_dict={self.x:next_state})

        action_index = self.possible_actions.index(action)
        next_action_index = self.possible_actions.index(next_action)

        if done:
            target[0][action_index] = reward
        else:
            target[0][action_index] = reward + \
                                      flags.discount_factor * next_q[0][next_action_index]

        self.sess.run(self.train, feed_dict={self.x: state, self.target: target})