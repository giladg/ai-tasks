import { useQuery } from '@tanstack/react-query';
import { taskService } from '../services/taskService';

export const useExtractionDates = () => {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['extraction-dates'],
    queryFn: () => taskService.getExtractionDates(),
  });

  return {
    dates: data || [],
    isLoading,
    error,
    refetch,
  };
};
