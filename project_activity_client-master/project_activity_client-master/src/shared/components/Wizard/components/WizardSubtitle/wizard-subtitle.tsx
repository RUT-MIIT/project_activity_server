import type { FC } from 'react';
import type { IWizardSubtitleProps } from '../../types/types';

import styles from './wizard-subtitle.module.scss';

export const WizardSubtitle: FC<IWizardSubtitleProps> = ({ text }) => {
	return <p className={styles.subtitle}>{text}</p>;
};
