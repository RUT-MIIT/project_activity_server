import type { FC } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import { CoordinationTabs } from './coordination-tabs';
import { CoordinationAppDetail } from './coordination-app-detail';
import { CoordinationActiveApps } from './coordination-active-apps';
import { useSelector } from '../../../store/store';

const CompletedApps = () => <div>Согласованные</div>;
const ReturnedApps = () => <div>На доработке</div>;
const CancelledApps = () => <div>Отклоненные</div>;

export const Coordination: FC = () => {
	const { applications } = useSelector((state) => state.coordination);

	return (
		<Routes>
			<Route path='tabs' element={<CoordinationTabs />}>
				<Route
					path='active'
					element={<CoordinationActiveApps apps={applications} />}
				/>
				<Route path='completed' element={<CompletedApps />} />
				<Route path='returned' element={<ReturnedApps />} />
				<Route path='cancelled' element={<CancelledApps />} />
				<Route index element={<Navigate to='active' replace />} />
			</Route>

			<Route path='app/:appId' element={<CoordinationAppDetail />} />
			<Route index element={<Navigate to='tabs' replace />} />
		</Routes>
	);
};
