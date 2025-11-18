import type { FC } from 'react';

import { useSelector } from '../../../../../store/store';

import { Field } from '../../../../../shared/components/Field/ui/field';
import { UserData } from './user-data';

import styles from '../styles/control-approve.module.scss';

export const DetailUserModal: FC = () => {
	const { currentApproveUser } = useSelector((state) => state.controlApprove);

	if (!currentApproveUser) {
		return <p>Пользователь не найден!</p>;
	}

	return (
		<div className={styles.form}>
			<UserData user={currentApproveUser} />
			{currentApproveUser.status === 'approved' ? (
				<>
					<Field
						title='Выбранная роль:'
						text={currentApproveUser.role?.name || ''}
					/>
					<Field
						title='Выбранное подразделение:'
						text={currentApproveUser.department?.name || ''}
					/>
				</>
			) : (
				<Field title='Причина отказа:' text={currentApproveUser.reason || ''} />
			)}
			<Field
				title='Решение по заявке:'
				text={`${currentApproveUser.actor?.full_name || ''} (${
					currentApproveUser.actor?.email || ''
				})`}
			/>
		</div>
	);
};
