import type { FC } from 'react';
import type { IUserDataProps } from '../types/types';
import type { IApproveUser } from '../../../../../store/control-approve/types';

import { Badge } from '../../../../../shared/components/Badge/ui/badge';

import { convertDate } from '../../../../../shared/lib/date';

import styles from '../styles/control-approve.module.scss';

export const UserData: FC<IUserDataProps> = ({ user }) => {
	const renderStatus = (user: IApproveUser) => {
		if (user.status === 'approved') {
			return <Badge text='Заявка одобрена' color='green' />;
		}
		if (user.status === 'rejected') {
			return <Badge text='Заявка отклонена' color='red' />;
		}
		return <Badge text='Ожидает решения' color='yellow' />;
	};

	return (
		<div className={styles.data} key={user.id}>
			<div className={styles.img}></div>
			<div className={styles.info}>
				<span className={styles.date}>{convertDate(user.created_at)}</span>
				<div className={styles.title}>
					<h4 className={styles.name}>
						{user.last_name} {user.first_name} {user.middle_name}
					</h4>
					{renderStatus(user)}
				</div>
				<div className={styles.contacts}>
					<p className={styles.text}>
						<span className={styles.text_weight_bold}>Почта: </span>
						{user.email}
					</p>
					<p className={styles.text}>
						<span className={styles.text_weight_bold}>Телефон: </span>
						{user.phone}
					</p>
				</div>
				<p className={styles.text}>
					<span className={styles.text_weight_bold}>Комментарий: </span>
					{user.comment}
				</p>
			</div>
		</div>
	);
};
