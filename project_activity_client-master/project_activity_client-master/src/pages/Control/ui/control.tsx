import type { FC } from 'react';

import { Routes, Route, Navigate } from 'react-router-dom';

import { Section } from '../../../shared/components/Section';
import { Tabs } from '../../../shared/components/Tabs/ui/tabs';
import { ControlApprove } from '../components/ControlApprove/ui/control-approve';

import { tabs } from '../lib/helpers';

const Users = () => <div>Пользователи</div>;
const Apps = () => <div>Заявки</div>;

export const Control: FC = () => {
	return (
		<Section
			sectionWidth='full'
			sectionTitle={{ text: 'Управление пользователями и заявками' }}>
			<Tabs tabs={tabs} />

			<Routes>
				<Route path='approve' element={<ControlApprove />} />
				<Route path='users' element={<Users />} />
				<Route path='apps' element={<Apps />} />

				<Route path='' element={<Navigate to='approve' replace />} />
			</Routes>
		</Section>
	);
};
