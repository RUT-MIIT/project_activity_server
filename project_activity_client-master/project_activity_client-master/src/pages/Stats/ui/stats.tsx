import type { FC } from 'react';

import { Section } from '../../../shared/components/Section';

export const Stats: FC = () => {
	return (
		<Section
			sectionWidth='full'
			sectionTitle={{ text: 'Статистика по заявкам' }}></Section>
	);
};
