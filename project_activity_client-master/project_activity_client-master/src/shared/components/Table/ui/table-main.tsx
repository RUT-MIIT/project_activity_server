import type { FC } from 'react';
import type { ITableProps } from '../types/types';

import styles from '../styles/table.module.scss';

export const TableMain: FC<ITableProps> = ({ children }) => {
	return <ul className={styles.table__main}>{children}</ul>;
};
