from Trainer import Trainer
import tensorflow as tf

if __name__ == "__main__":
	filename = "model_final"
	trainer = Trainer()
	
	trainer.train()
	trainer.evaluate()

	trainer.save_model(filename)