import type { FC } from 'react';
import type { IApproveUser } from '../../../../../store/control-approve/types';

import { useEffect } from 'react';
import { useDispatch, useSelector } from '../../../../../store/store';

import { Preloader } from '../../../../../shared/components/Preloader/ui/preloader';
import { Button } from '../../../../../shared/components/Button/ui/button';
import { Modal } from '../../../../../shared/components/Modal/ui/modal';
import { UserData } from './user-data';
import { ApproveUserForm } from './approve-user-form';
import { RejectUserForm } from './reject-user-form';
import { DetailUserModal } from './detail-user-modal';

import { getApproveUsersAction } from '../../../../../store/control-approve/actions';
import {
	getDepartmentsAction,
	getRolesAction,
} from '../../../../../store/catalog/actions';
import {
	setCurrentApproveUser,
	openApproveModal,
	openRejectModal,
	openDetailModal,
	closeModals,
} from '../../../../../store/control-approve/reducer';

import styles from '../styles/control-approve.module.scss';

export const ControlApprove: FC = () => {
	const dispatch = useDispatch();
	const {
		approveUsers,
		isOpenApproveModal,
		isOpenRejectModal,
		isOpenDetailModal,
		isLoadingApprove,
	} = useSelector((state) => state.controlApprove);
	const { isLoadingCatalog } = useSelector((state) => state.catalog);

	const handleOpenApproveModal = (user: IApproveUser) => {
		dispatch(setCurrentApproveUser(user));
		dispatch(openApproveModal());
	};

	const handleOpenRejectModal = (user: IApproveUser) => {
		dispatch(setCurrentApproveUser(user));
		dispatch(openRejectModal());
	};

	const handleOpenDetailModal = (user: IApproveUser) => {
		dispatch(setCurrentApproveUser(user));
		dispatch(openDetailModal());
	};

	const handleCloseModals = () => {
		dispatch(closeModals());
	};

	useEffect(() => {
		dispatch(getApproveUsersAction());
		dispatch(getDepartmentsAction());
		dispatch(getRolesAction());
	}, [dispatch]);

	if (isLoadingApprove || isLoadingCatalog) {
		return <Preloader />;
	}

	if (!approveUsers.length && !isLoadingApprove) {
		return <p>Нет пользователей для одобрения.</p>;
	}

	return (
		<div className={styles.container}>
			<ul className={styles.list}>
				{approveUsers.map((user: IApproveUser) => (
					<li className={styles.item} key={user.id}>
						<UserData user={user} />
						{user.status === 'submitted' ? (
							<div className={styles.buttons}>
								<Button
									text='Одобрить'
									onClick={() => handleOpenApproveModal(user)}
								/>
								<Button
									text='Отклонить'
									onClick={() => handleOpenRejectModal(user)}
								/>
							</div>
						) : (
							<Button
								text='Подробнее'
								onClick={() => handleOpenDetailModal(user)}
							/>
						)}
					</li>
				))}
			</ul>
			{isOpenApproveModal && (
				<Modal
					isOpen={isOpenApproveModal}
					onClose={handleCloseModals}
					title='Одобрить пользователя'>
					<ApproveUserForm />
				</Modal>
			)}
			{isOpenRejectModal && (
				<Modal
					isOpen={isOpenRejectModal}
					onClose={handleCloseModals}
					title='Отклонить пользователя'>
					<RejectUserForm />
				</Modal>
			)}
			{isOpenDetailModal && (
				<Modal
					isOpen={isOpenDetailModal}
					onClose={handleCloseModals}
					title='Информация о заявке'>
					<DetailUserModal />
				</Modal>
			)}
		</div>
	);
};
