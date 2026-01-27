import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';

export const useAuthStatus = () => {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['auth-status'],
    queryFn: () => authService.getAuthStatus(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });

  return {
    authStatus: data,
    isLoading,
    error,
    refetchAuthStatus: refetch,
    hasDataAccess: data?.has_data_access || false,
    needsAuthorization: data?.authenticated && !data?.has_data_access,
  };
};
