import type { FC } from 'react';

import { useDispatch, useSelector } from '../../../store/store';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { Section } from '../../../shared/components/Section';
import { Preloader } from '../../../shared/components/Preloader/ui/preloader';
import { EditApplication } from '../../../widgets/EditApplication/ui/edit-application';

import { getCoordinationAppDetailAction } from '../../../store/coordination/actions';

export const CoordinationAppDetail: FC = () => {
	const dispatch = useDispatch();
	const { applicationDetail, isLoadingDetail } = useSelector(
		(state) => state.coordination
	);

	const { appId } = useParams<{ appId: string }>();

	useEffect(() => {
		if (appId) {
			dispatch(getCoordinationAppDetailAction(appId));
		}
	}, [dispatch, appId]);

	if (isLoadingDetail) return <Preloader />;

	return (
		<Section
			sectionWidth='full'
			sectionTitle={{
				text: applicationDetail?.title || '',
			}}
			sectionDescription='Обновите данные или оставьте комментарии для поля'
			withHeaderMargin>
			<EditApplication />
		</Section>
	);
};
