python run_knowledge_representation.py -data_path ~/Github/joint-kg-recommender/datasets/ -log_path ~/Github/joint-kg-recommender/log/ -kg_test_files valid.dat:test.dat -l2_lambda 1e-5 -negtive_samples 1 -model_type transh -nohas_visualization -dataset ml1m -batch_size 637 -embedding_size 100 -learning_rate 0.005 -topn 10 -seed 3 -eval_interval_steps 1250