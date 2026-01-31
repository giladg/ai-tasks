import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { taskService } from '../services/taskService';
import { TaskUpdate, TaskFilters } from '../types/task';

export const useTasks = (filters?: TaskFilters) => {
  const queryClient = useQueryClient();

  // Fetch tasks
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => taskService.getTasks(filters),
  });

  // Update task mutation
  const updateTaskMutation = useMutation({
    mutationFn: ({ id, update }: { id: number; update: TaskUpdate }) =>
      taskService.updateTask(id, update),
    onSuccess: () => {
      // Invalidate and refetch tasks
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Delete task mutation
  const deleteTaskMutation = useMutation({
    mutationFn: (id: number) => taskService.deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  // Trigger sync mutation
  const triggerSyncMutation = useMutation({
    mutationFn: () => taskService.triggerSync(),
    onSuccess: () => {
      // Refetch tasks after sync
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
      }, 2000); // Wait 2 seconds for sync to process
    },
  });

  // Wrapper functions to match expected signatures
  const updateTask = (id: number, update: TaskUpdate) => {
    updateTaskMutation.mutate({ id, update });
  };

  const deleteTask = (id: number) => {
    deleteTaskMutation.mutate(id);
  };

  const triggerSync = async () => {
    await triggerSyncMutation.mutateAsync();
  };

  return {
    tasks: data?.tasks || [],
    total: data?.total || 0,
    isLoading,
    error,
    refetch,
    updateTask,
    deleteTask,
    triggerSync,
    isUpdating: updateTaskMutation.isPending,
    isDeleting: deleteTaskMutation.isPending,
    isSyncing: triggerSyncMutation.isPending,
  };
};
