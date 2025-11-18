import type { FC, ReactElement } from 'react';

import { EPAGESROUTES } from '../../utils/routes';

import { useSelector } from '../../../store/store';
import { getIsAuthChecked, getUser } from '../../../store/user/reducer';
import { Navigate, useLocation } from 'react-router-dom';

import { Preloader } from '../Preloader/ui/preloader';

interface IProtectedProps {
	onlyUnAuth?: boolean;
	component: ReactElement;
}

const Protected: FC<IProtectedProps> = ({ onlyUnAuth = false, component }) => {
	const isAuthChecked = useSelector(getIsAuthChecked);
	const user = useSelector(getUser);
	const location = useLocation();

	if (!isAuthChecked) {
		return <Preloader />;
	}

	if (!onlyUnAuth && !user) {
		return <Navigate to={EPAGESROUTES.LOGIN} state={{ from: location }} />;
	}

	if (onlyUnAuth && user) {
		/* const { from } = location.state ?? { from: { pathname:  } };
		console.log(from); */
		return <Navigate to={EPAGESROUTES.MAIN} />;
	}

	if (user) {
		if (location.pathname === '/') {
			return <Navigate to={EPAGESROUTES.MAIN} />;
		}
	}

	return component;
};

export const OnlyAuth = Protected;
export const OnlyUnAuth = ({ component }: { component: ReactElement }) => (
	<Protected onlyUnAuth={true} component={component} />
);
