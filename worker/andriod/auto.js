/*
 * @Date: 2024-08-06 10:19:17
 * @LastEditors: 牛智超
 * @LastEditTime: 2024-08-06 10:30:14
 * @FilePath: \tbScripte\worker\auto.js
 */
const amqp = require('amqplib/callback_api');

const WORKER_ID = 'worker-' + Math.random().toString(36).substring(7);  // 每个客户端的唯一标识
const rabbitmq_host = 'amqp://localhost';
const task_queue = 'task_queue';
const result_queue = 'result_queue';

function executeTask(task) {
    console.log(`Worker ${WORKER_ID} is executing task: ${task.description}`);
    // 示例任务：打开淘宝，搜索关键字
    if (task.description.includes('淘宝')) {
        // 模拟任务执行过程
        setTimeout(() => {
            console.log(`Worker ${WORKER_ID} completed task: ${task.description}`);
            completeTask(task.id);
        }, 15000);  // 模拟任务执行时间
    }
}

function completeTask(taskId) {
    const result = {
        task_id: taskId,
        worker_id: WORKER_ID,
        status: 'completed',
        end_time: new Date().toISOString()
    };
    publishResult(result);
}

function publishResult(result) {
    amqp.connect(rabbitmq_host, function(error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function(error1, channel) {
            if (error1) {
                throw error1;
            }
            channel.assertQueue(result_queue, { durable: false });
            channel.sendToQueue(result_queue, Buffer.from(JSON.stringify(result)));
        });

        setTimeout(function() {
            connection.close();
        }, 500);
    });
}

function getTasks() {
    amqp.connect(rabbitmq_host, function(error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function(error1, channel) {
            if (error1) {
                throw error1;
            }
            channel.assertQueue(task_queue, { durable: false });

            console.log(`Worker ${WORKER_ID} is waiting for tasks in ${task_queue}. To exit press CTRL+C`);
            channel.consume(task_queue, function(msg) {
                if (msg !== null) {
                    const task = JSON.parse(msg.content.toString());
                    if (task.workers.length < task.worker_limit) {
                        task.workers.push(WORKER_ID);
                        console.log(`Worker ${WORKER_ID} received task: ${task.description}`);
                        executeTask(task);
                        channel.ack(msg);
                    } else {
                        channel.reject(msg, true);
                    }
                }
            });
        });
    });
}

// 开始获取任务
getTasks();
