import { buildSearchEngine } from '@coveo/headless';

export const engine = buildSearchEngine({
  configuration: {
    organizationId: import.meta.env.VITE_COVEO_ORG_ID,
    accessToken: import.meta.env.VITE_COVEO_API_KEY,
  },
});
