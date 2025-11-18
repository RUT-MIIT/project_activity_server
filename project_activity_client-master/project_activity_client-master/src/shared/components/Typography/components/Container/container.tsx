import type { FC } from 'react';
import type { IContainerProps } from '../../types/types';

import styles from '../../styles/typography.module.scss';

export const Container: FC<IContainerProps> = ({ children }) => {
	return <div className={styles.container}>{children}</div>;
};
