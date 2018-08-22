""" battle of two armies """

import magent


def get_config(map_size):
    gw = magent.gridworld
    cfg = gw.Config()

    cfg.set({"map_width": map_size, "map_height": map_size})
    cfg.set({"minimap_mode": True})
    cfg.set({"embedding_size": 10})

    marine = cfg.register_agent_type(
        "marine",
        {'width': 1, 'length': 1, 'hp': 10, 'speed': 2,
         'view_range': gw.CircleRange(6), 'attack_range': gw.CircleRange(1.5),
         'damage': 2, 'step_recover': 0.0,

         'step_reward': -0.01,  'kill_reward': 5, 'dead_penalty': -0.1, 'attack_penalty': -0.1,
         })
    marine2 = cfg.register_agent_type(
        "marine2",
        {'width': 1, 'length': 1, 'hp': 10, 'speed': 2,
         'view_range': gw.CircleRange(6), 'attack_range': gw.CircleRange(1.5),
         'damage': 2, 'step_recover': 0.0,
         # alliance's id, value of g2
         'ally_with': 2,

         'step_reward': -0.01,  'kill_reward': 5, 'dead_penalty': -0.1, 'attack_penalty': -0.1,
         })

    """
    if the damage in lower then 0, the enemy's hp increases when attack
    """
    medic = cfg.register_agent_type(
        "medic",
        {'width': 1, 'length': 1, 'hp': 10, 'speed': 2,
         'view_range': gw.CircleRange(6), 'attack_range': gw.CircleRange(1.5),
         'damage': -2, 'step_recover': 0.0,
         # value of g1
         'ally_with': 1,

         'step_reward': -0.01, 'kill_reward': 5, 'dead_penalty': -0.1, 'attack_penalty': -0.1,
         })

    g0 = cfg.add_group(marine)
    g1 = cfg.add_group(marine2)
    g2 = cfg.add_group(medic)

    a = gw.AgentSymbol(g0, index='any')
    b = gw.AgentSymbol(g1, index='any')
    c = gw.AgentSymbol(g2, index='any')

    # a rule
    cfg.add_reward_rule(gw.Event(a, 'attack', b), receiver=a, value=2)
    cfg.add_reward_rule(gw.Event(a, 'attack', c), receiver=a, value=3)

    cfg.add_reward_rule(gw.Event(a, 'kill', b), receiver=a, value=10)
    cfg.add_reward_rule(gw.Event(a, 'kill', c), receiver=a, value=20)

    # b rule
    cfg.add_reward_rule(gw.Event(b, 'attack', a), receiver=b, value=2)
    cfg.add_reward_rule(gw.Event(b, 'kill', a), receiver=b, value=10)

    # c rule
    cfg.add_reward_rule(gw.Event(c, 'attack', b), receiver=c, value=3)

    return cfg
