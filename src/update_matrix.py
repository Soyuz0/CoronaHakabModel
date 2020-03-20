
class UpdateMatrixManager:
    """
    Manages the "Update Matrix" stage of the simulation.
    """
    
    def __init__():
        pass
    
    def update_matrix_step(self, matrix, family_matrix, sick_agents_vector, agents_list):
        """
        Update the matrix step
        """
        # for now, we will not update the matrix at all
        # self.apply_self_quarantine(matrix, family_matrix, sick_agents_vector, agents_list)
        
        return
        
    def apply_self_quarantine(self, matrix, family_matrix, sick_agents_vector, agents_list):
        """
        Modifies the matrix so self quarantines are in place
        """
        sick_agents_ids = sick_agents_vector.get_sick_ids()
        
        # run on all self quarantined agents
        for agent_id in sick_agents_ids:
            if agents_list[agent_id].is_self_quarantined():
                # remove all existing relations
                matrix.zero_column(agent_id)
                # insert only family relations (as he is at home)
                matrix.add_to_column(family_matrix.get_column(agent_id))
                
                
    