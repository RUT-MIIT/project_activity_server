import type { FC } from 'react';

import { Section } from '../../../../shared/components/Section/ui/section';
import { CreateMainApplication } from '../../../../widgets/CreateApplication/ui/create-main-application';

export const NewApp: FC = () => {
	return (
		<Section
			sectionWidth='full'
			sectionHeight='page'
			sectionTitle={{ text: 'Создание новой заявки' }}
			sectionDescription='Заполните несколько шагов, чтобы отправить заявку на рассмотрение'>
			<CreateMainApplication />
		</Section>
	);
};
