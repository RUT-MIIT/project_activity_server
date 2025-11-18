import type { FC } from 'react';
import type { ITableTextProps } from '../types/types';

import styles from '../styles/table-text.module.scss';

export const TableText: FC<ITableTextProps> = ({ text, type = 'default' }) => {
	return (
		<p
			className={`${styles.text} ${
				type === 'empty' ? styles.text_type_empty : ''
			}`}>
			{text}
		</p>
	);
};
