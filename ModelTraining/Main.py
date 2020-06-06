from Trainer import Trainer
import tensorflow as tf

if __name__ == "__main__":
	
	minAccuracy = 0.95
	accuracy = 0
	while accuracy < minAccuracy:
		trainer = Trainer()
		trainer.train()
		accuracy = trainer.evaluate()
