
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Metrics {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column({ type: "varchar", nullable: true})
    browser: number;

    @Column({ type: "varchar", nullable: true })
    acceptLanguage: string;

    @Column({ type: "timestamp" , nullable: true})
    time: string;

    @Column({ type: "varchar", nullable: true })
    host: string;

    @Column({ type: "varchar", nullable: true })
    short: string;

    @Column({ type: "varchar", nullable: true })
    original: string;

    @Column({ type: "varchar" })
    eventId: string;
}
