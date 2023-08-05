from gym.envs.registration import register
import dm_gym

register(id='clustering-v0',
         entry_point='dm_gym.envs.clustering.clustering_env_v0:ClusteringEnv_0')
register(id='clustering-v1',
         entry_point='dm_gym.envs.clustering.clustering_env_v1:ClusteringEnv_1')
register(id='clustering-v2',
         entry_point='dm_gym.envs.clustering.clustering_env_v2:ClusteringEnv_2')
register(id='clustering-v3',
         entry_point='dm_gym.envs.clustering.clustering_env_v3:ClusteringEnv_3')
register(id='classification-v0',
         entry_point='dm_gym.envs.classification.classification_env_v0:ClassificationEnv_0')

#register(id='basic-v2', entry_point='gym_basic.envs:BasicEnv2',)
