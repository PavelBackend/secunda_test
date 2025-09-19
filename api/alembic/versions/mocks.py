from alembic import op

revision = "mocks"
down_revision = "enable_geo"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO building (address, location)
        VALUES
          ('Main Street 1', ST_SetSRID(ST_MakePoint(37.618423, 55.751244), 4326)::geography),
          ('Main Street 2', ST_SetSRID(ST_MakePoint(37.619000, 55.752000), 4326)::geography),
          ('Main Street 3', ST_SetSRID(ST_MakePoint(30.3350986, 59.9342802), 4326)::geography)
        ON CONFLICT (address) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO activity (name, parent_id) VALUES
          ('IT Services', NULL),
          ('Education',   NULL),
          ('Healthcare',  NULL)
        ON CONFLICT (name) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO activity (name, parent_id) VALUES
          ('Web Development',    (SELECT id FROM activity WHERE name='IT Services')),
          ('Mobile Development', (SELECT id FROM activity WHERE name='IT Services')),
          ('School Education',   (SELECT id FROM activity WHERE name='Education')),
          ('University Education',(SELECT id FROM activity WHERE name='Education')),
          ('Clinic',             (SELECT id FROM activity WHERE name='Healthcare'))
        ON CONFLICT (name) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO activity (name, parent_id) VALUES
          ('Frontend',         (SELECT id FROM activity WHERE name='Web Development')),
          ('Backend',          (SELECT id FROM activity WHERE name='Web Development')),
          ('iOS',              (SELECT id FROM activity WHERE name='Mobile Development')),
          ('Android',          (SELECT id FROM activity WHERE name='Mobile Development')),
          ('Primary School',   (SELECT id FROM activity WHERE name='School Education')),
          ('High School',      (SELECT id FROM activity WHERE name='School Education')),
          ('General Medicine', (SELECT id FROM activity WHERE name='Clinic'))
        ON CONFLICT (name) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO organization (name, building_id) VALUES
          ('Test Org 1', (SELECT id FROM building WHERE address='Main Street 1')),
          ('Test Org 2', (SELECT id FROM building WHERE address='Main Street 1')),
          ('Test Org 3', (SELECT id FROM building WHERE address='Main Street 2')),
          ('Test Org 4', (SELECT id FROM building WHERE address='Main Street 3')),
          ('Test Org 5', (SELECT id FROM building WHERE address='Main Street 3'))
        ON CONFLICT (name) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO organization_activity (organization_id, activity_id)
        SELECT o.id, a.id
        FROM (VALUES
            ('Test Org 1','Web Development'),
            ('Test Org 1','Frontend'),
            ('Test Org 2','University Education'),
            ('Test Org 2','High School'),
            ('Test Org 3','Mobile Development'),
            ('Test Org 3','Android'),
            ('Test Org 4','Clinic'),
            ('Test Org 4','General Medicine'),
            ('Test Org 5','School Education'),
            ('Test Org 5','Primary School')
        ) as x(org_name, act_name)
        JOIN organization o ON o.name = x.org_name
        JOIN activity     a ON a.name = x.act_name
        ON CONFLICT DO NOTHING;
    """)

    op.execute("""
        INSERT INTO phone (number, organization_id)
        SELECT v.number, o.id
        FROM (
            VALUES
                ('+7-999-111-1111','Test Org 1'),
                ('+7-999-222-2222','Test Org 1'),
                ('+7-999-333-3333','Test Org 2'),
                ('+7-999-444-4444','Test Org 3'),
                ('+7-999-555-5555','Test Org 4'),
                ('+7-999-666-6666','Test Org 5')
        ) AS v(number, org_name)
        JOIN organization o ON o.name = v.org_name
        LEFT JOIN phone p ON p.number = v.number
        WHERE p.id IS NULL;  -- анти-join, не вставляем дубликаты
    """)


def downgrade():
    # op.execute("""
    #     DELETE FROM phone
    #     WHERE number IN (
    #       '+7-999-111-1111', '+7-999-222-2222', '+7-999-333-3333',
    #       '+7-999-444-4444', '+7-999-555-5555', '+7-999-666-6666'
    #     );
    # """)

    # op.execute("""
    #     DELETE FROM organization_activity
    #     WHERE organization_id IN (
    #       SELECT id FROM organization
    #       WHERE name IN ('Test Org 1','Test Org 2','Test Org 3','Test Org 4','Test Org 5')
    #     );
    # """)

    # op.execute("""
    #     DELETE FROM organization
    #     WHERE name IN ('Test Org 1','Test Org 2','Test Org 3','Test Org 4','Test Org 5');
    # """)

    # op.execute("""
    #     DELETE FROM activity
    #     WHERE name IN (
    #       'Frontend','Backend','iOS','Android','Primary School','High School','General Medicine',
    #       'Web Development','Mobile Development','School Education','University Education','Clinic',
    #       'IT Services','Education','Healthcare'
    #     );
    # """)

    # op.execute("""
    #     DELETE FROM building
    #     WHERE address IN ('Main Street 1','Main Street 2','Main Street 3');
    # """)
  pass