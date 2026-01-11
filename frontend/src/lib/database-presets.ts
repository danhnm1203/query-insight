import { Database, Server, Layers } from 'lucide-react'

export const DATABASE_PRESETS = {
    postgresql: {
        name: 'PostgreSQL',
        type: 'postgres',
        port: 5432,
        defaultConnectionString: 'postgresql://username:password@localhost:5432/database',
        icon: Database,
        description: 'Popular open-source relational database',
    },
    mysql: {
        name: 'MySQL',
        type: 'mysql',
        port: 3306,
        defaultConnectionString: 'mysql://username:password@localhost:3306/database',
        icon: Server,
        description: 'World\'s most popular open-source database',
    },
    mongodb: {
        name: 'MongoDB',
        type: 'mongodb',
        port: 27017,
        defaultConnectionString: 'mongodb://username:password@localhost:27017/database',
        icon: Layers,
        description: 'Document-oriented NoSQL database',
    },
} as const

export type DatabasePresetKey = keyof typeof DATABASE_PRESETS
