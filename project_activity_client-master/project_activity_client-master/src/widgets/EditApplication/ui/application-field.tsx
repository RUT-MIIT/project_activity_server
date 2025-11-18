import type { FC } from 'react';
import type { IApplicationFieldProps } from '../types/types';

import styles from '../styles/edit-application.module.scss';

export const ApplicationField: FC<IApplicationFieldProps> = ({
	title,
	fieldCode,
	currentField,
	getCommentCount,
	onSelectField,
	children,
}) => {
	const isActive = currentField?.code === fieldCode;

	return (
		<div
			className={`${styles.field} ${isActive ? styles.field_active : ''}`}
			onClick={() => onSelectField({ name: title, code: fieldCode })}>
			<div className={styles.field__header}>
				<h4 className={styles.field__title}>{title}</h4>
				<div
					className={`${styles.field__comments} ${
						isActive ? styles.field__comments_active : ''
					}`}>
					{getCommentCount(fieldCode)}
				</div>
			</div>
			{children}
		</div>
	);
};
