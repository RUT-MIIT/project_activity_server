import type { FC } from 'react';
import type { IWizardMainProps } from '../../types/types';

import styles from './wizard-main.module.scss';

export const WizardMain: FC<IWizardMainProps> = ({ children }) => {
	return <div className={styles.container}>{children}</div>;
};
