import type { FC } from 'react';
import type { IWizardTitleProps } from '../../types/types';

import styles from './wizard-title.module.scss';

export const WizardTitle: FC<IWizardTitleProps> = ({ text }) => {
	return <h2 className={styles.title}>{text}</h2>;
};
