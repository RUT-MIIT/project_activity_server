import { Route, Routes, useLocation } from 'react-router-dom';
import { useEffect } from 'react';

import { useDispatch } from '../store/store';
import {
	OnlyUnAuth,
	OnlyAuth,
} from '../shared/components/ProtectedRoute/protected-route';

import { Login } from '../pages/Login/ui/login';
import { Registration } from '../pages/Registration/ui/registration';
import { ForgotPassword } from '../pages/ForgotPassword/ui/forgot-password';
import { NotFound } from '../pages/NotFound/ui/not-found';
import { Home } from '../pages/Home/ui/home';
import { NewApp } from '../pages/Application/NewApp/ui/new-app';
import { MyApp } from '../pages/Application/MyApp/ui/my-app';
import { Coordination } from '../pages/Coordination/ui/coordination';
import { Stats } from '../pages/Stats/ui/stats';
import { Control } from '../pages/Control/ui/control';

import { EPAGESROUTES, EMAINROUTES } from '../shared/utils/routes';
import { checkUserAuth } from '../store/user/actions';

import { MainLayout } from '../shared/components/Layout/MainLayout/ui/main-layout';

import styles from './app.module.scss';

export const App = () => {
	const dispatch = useDispatch();
	const location = useLocation();
	const background = location.state && location.state.background;

	useEffect(() => {
		dispatch(checkUserAuth());
	}, [dispatch]);

	return (
		<div className={styles.page}>
			<Routes location={background || location}>
				<Route
					path={EPAGESROUTES.MAIN}
					element={<OnlyAuth component={<MainLayout />} />}>
					<Route path={EMAINROUTES.HOME} element={<Home />} />
					<Route path={EMAINROUTES.NEW_APP} element={<NewApp />} />
					<Route path={EMAINROUTES.MY_APPS} element={<MyApp />} />
					<Route
						path={`${EMAINROUTES.COORDINATION}/*`}
						element={<Coordination />}
					/>
					<Route path={EMAINROUTES.STATS} element={<Stats />} />
					<Route path={`${EMAINROUTES.CONTROL}/*`} element={<Control />} />
					<Route path='*' element={<NotFound />} />
				</Route>

				<Route
					path={EPAGESROUTES.LOGIN}
					element={<OnlyUnAuth component={<Login />} />}
				/>
				<Route
					path={EPAGESROUTES.REGISTRATION}
					element={<OnlyUnAuth component={<Registration />} />}
				/>
				<Route
					path={EPAGESROUTES.FORGOT_PASSWORD}
					element={<OnlyUnAuth component={<ForgotPassword />} />}
				/>
				<Route path='*' element={<NotFound />} />
			</Routes>
			<div id='modal-root'></div>
		</div>
	);
};
