import type { FC } from 'react';
import type { ITableProps } from '../types/types';

import styles from '../styles/table.module.scss';

export const Table: FC<ITableProps> = ({ children }) => {
	return <div className={styles.table}>{children}</div>;
};
