import os


class JobState(object):
    QUEUED = 'queued'
    FINISHED = 'finished'
    FAILED = 'failed'
    STARTED = 'started'
    DEFERRED = 'deferred'
    ABORTED = 'aborted'
    NOT_FOUND = "not_found"


class Config(object):
    db_timeout = 10 * 1000

    # index names
    QA = "qa"
    QQ = "qq"
    AUTO = "autocomplete"

    log_collection = "soco_logs"
    task_collection = "soco_tasks"
    user_collection = "soco_users"
    op_collection = "soco_ops"
    key_collection = "keys"
    file_collection = 'soco_files'
    activity_collection = "soco_activities"
    feedback_collection = "soco_feedback"
    plan_collection = "soco_plans"

    # database
    soco_db = "trainer"
    db_name = "trainer"
    index_collection = "soco_indexes"
    publish_log_collection = "publish_logs"
    init_collection = "soco_init"

    # index status
    EMPTY = "empty"
    NOT_FOUND = "not_found"
    UPDATE = 'updating'
    QUEUED = "queued"
    READY = "ready"
    ABORT = "abort"

    # index code
    ERROR = "error"
    SUCCESS = 'success'


class EnvVars(object):
    # system configuration
    region = os.environ.get("REGION", 'us').lower()
    max_batch_size = int(os.environ.get('MAX_BATCH_SIZE', 500))
    redis_queues = os.environ.get('REDIS_QUEUES', 'trainer').split(';')
    mongodb_ssl = os.environ.get('MONGODB_SSL')
    minio_access_key = os.environ.get('MINIO_ACCESS_KEY')
    minio_secret_key = os.environ.get('MINIO_SECRET_KEY')
    storange_server_uri = os.environ.get('STORAGE_SERVER_URI')
    max_num_index = int(os.environ.get('MAX_NUM_INDEX', 2))
    job_ttl = os.environ.get("JOB_TTL", "48h")
    op_ttl = max(int(os.environ.get('OP_TTL', 432000)), 3600)
    remote_server_uri = os.environ.get('REMOTE_SERVER_URI')
    mode = os.environ.get('MODE', "k8s")