import dm_gym


def ray_create_env(config, *args, **kwargs):

    if type(config) == dict:
        env_name = config['env']
    else:
        env_name = config
    if env_name == 'clustering-v0':
        from dm_gym.envs.clustering.clustering_env_v0 import ClusteringEnv_0 as env
    elif env_name == 'clustering-v1':
        from dm_gym.envs.clustering.clustering_env_v1 import ClusteringEnv_1 as env
    elif env_name == 'clustering-v2':
        from dm_gym.envs.clustering.clustering_env_v2 import ClusteringEnv_2 as env
    elif env_name == 'clustering-v3':
        from dm_gym.envs.clustering.clustering_env_v3 import ClusteringEnv_3 as env
    elif env_name == 'classification-v0':
        from dm_gym.envs.classification.classification_env_v0 import ClassificationEnv_0 as env
    else:
        raise NotImplementedError(
            'Environment {} not recognized.'.format(env_name))
    return env


def create_env(name, *args, **kwargs):
    if name == "clustering-v0":
        env = dm_gym.make("dm_gym:clustering-v0", **kwargs)
    elif name == "clustering-v1":
        env = dm_gym.make("dm_gym:clustering-v1", **kwargs)
    elif name == "clustering-v2":
        env = dm_gym.make("dm_gym:clustering-v2", **kwargs)
    elif name == "clustering-v3":
        env = dm_gym.make("dm_gym:clustering-v3", **kwargs)
    elif name == "classification-v0":
        env = dm_gym.make("dm_gym:classification-v0", **kwargs)
    else:
        raise NotImplementedError(
            'Environment {} not recognized.'.format(name))

    return env
