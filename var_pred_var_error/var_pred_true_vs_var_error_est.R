# input arguments to simulate simple linear regression
NUM_SAMPLES = 100
NUM_EXAMPLES = 500
TRAIN_RATIO = 0.5
ERROR_SD = 2
X_LB = 0; X_UB = 10
INTERCEPT = 0; SLOPE = 1
POLYNOMIAL_DEGREES = 1:6
# my compute_var_preds code can't handle degrees > 6
# b/c it directly computes an inverse
SEED = 42


# fixed data and parameters
ERROR_VAR = ERROR_SD^2
x = runif(NUM_EXAMPLES, min=X_LB, max=X_UB)
beta = c(INTERCEPT, SLOPE)
y_true_mean = cbind(1, x) %*% beta


compute_var_preds = function(X_tr, X_te, error_var=ERROR_VAR) {
  # Returns sum of true variances of test set predictions using
  # an analytical formula.
  # TODO: instead grab diag of inverse using a numerical solver
  # that isn't just the inverse!
  X_tr = as.matrix(X_tr)
  X_te = as.matrix(X_te)
  XtX_inv = solve(t(X_tr) %*% X_tr)
  true_var_preds = ERROR_VAR*diag((X_te %*% XtX_inv %*% t(X_te)))
  return(sum(true_var_preds))
}


# loop takes 5-10 seconds
mses = matrix(rep(NA, NUM_SAMPLES*length(POLYNOMIAL_DEGREES)),
              nrow=NUM_SAMPLES,
              ncol=length(POLYNOMIAL_DEGREES))
var_preds = matrix(rep(NA, NUM_SAMPLES*length(POLYNOMIAL_DEGREES)),
                   nrow=NUM_SAMPLES,
                   ncol=length(POLYNOMIAL_DEGREES))
for (i in 1:NUM_SAMPLES) {
  j = 1 # indexes degree
  for (degree in POLYNOMIAL_DEGREES) {
    # x - polynomial transform, handle degree=0
    if (degree == 0) {
      X_poly = data.frame(x=rep(1, length(x)))
    } else {
      X_poly = data.frame(poly(x, degree=degree, raw=TRUE))
    }
    # y - randomly generate
    set.seed(SEED*i*j)
    error = rnorm(NUM_EXAMPLES, mean=0, sd=ERROR_SD)
    y = y_true_mean + error
    # split into train and test
    tr_inds = sample(NUM_EXAMPLES, floor(NUM_EXAMPLES*TRAIN_RATIO))
    y_tr = y[tr_inds]
    y_te = y[-tr_inds]
    X_tr = X_poly[tr_inds,,drop=FALSE] # keep the df's row names
    X_te = X_poly[-tr_inds,,drop=FALSE]
    # fit, predict
    model = lm(y_tr ~ ., data=X_tr)
    # suppress warnings about predictions from rank-deficient fit.
    # should only occur for degree 0, but whatever...
    y_tr_pred = suppressWarnings(predict(model, X_tr, type="response"))
    y_te_pred = suppressWarnings(predict(model, X_te, type="response"))
    # store results
    var_preds[i,j] = compute_var_preds(X_tr, X_te)
    mses[i,j] = mean((y_te - y_te_pred)^2)
    j = j+1
  }
}


# conclusion
var_preds_mean = apply(var_preds, MARGIN=2,
                       FUN=mean) # randomness in splits. aggregate w/ mean
var_mses_estimates = apply(mses, MARGIN=2, FUN=var)

# final plot of interest
poly_degree_col = 'red'
plot(var_preds_mean, var_mses_estimates,
     xlab='true total Var(predictions)',
     ylab='estimated Var(test MSE)',
     pch=16, cex=1)
text(var_preds_mean, var_mses_estimates,
     POLYNOMIAL_DEGREES, pos=2, col=poly_degree_col)
legend('bottomleft',
       legend='polynomial degree',
       text.col=poly_degree_col)

# misc plots
# boxplot(mses,
#         names=POLYNOMIAL_DEGREES,
#         xlab='polynomial degree',
#         ylab='test MSE')

# visual check for degree of overfitting for the last degree
# x_tr = x[tr_inds]
# plot(x_tr, y_tr,
#      xlab='x (train)',
#      ylab='y (train)',
#      main=paste('polynomial degree:', degree))
# x_tr_order = order(x_tr) # to plot preds as a line, need x to be sorted
# lines(x_tr[x_tr_order],
#       y_tr_pred[x_tr_order])