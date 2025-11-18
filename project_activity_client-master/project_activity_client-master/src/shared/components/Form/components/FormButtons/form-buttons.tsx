import type { FC } from 'react';
import type { IFormButtonsProps } from '../../types/types';

import styles from './form-buttons.module.scss';

export const FormButtons: FC<IFormButtonsProps> = ({ children }) => {
	return <div className={styles.container}>{children}</div>;
};
