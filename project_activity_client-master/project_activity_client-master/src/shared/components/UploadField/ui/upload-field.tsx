import type { FC, ChangeEvent } from 'react';

import { GetBase64File } from '../../../lib/getBase64File';

import styles from '../styles/upload-field.module.scss';

export interface IUploadFile {
	base64: string | ArrayBuffer | null;
	name: string;
}

export interface IUploadFileProps {
	file: IUploadFile | null;
	onChange: (file: IUploadFile) => void;
}

export const UploadField: FC<IUploadFileProps> = ({ file, onChange }) => {
	const handleChangeTask = (e: ChangeEvent<HTMLInputElement>) => {
		if (e.target.files && e.target.files.length > 0) {
			const file = e.target.files[0];
			GetBase64File(file)
				.then((result) => {
					const fileWithBase64 = {
						name: file.name,
						base64: result,
					};
					onChange(fileWithBase64);
				})
				.catch((err) => {
					console.error('Error while reading the file:', err);
				});
		}
	};

	return (
		<div className={styles.container}>
			<label htmlFor='upload-file' className={styles.field}>
				<p className={styles.caption}>{file ? file.name : 'Выберите файл..'}</p>
				<div className={styles.icon}></div>
			</label>
			<input
				onChange={handleChangeTask}
				id='upload-file'
				className={styles.input}
				type='file'
			/>
		</div>
	);
};
